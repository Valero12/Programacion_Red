import socket
import threading

# Variable compartida y su candado (sección crítica)
turno_actual = 0
lock_turno = threading.Lock()

def atender_cliente_tcp(conexion, direccion):
    """Atiende la solicitud de turno de un cliente por TCP."""
    global turno_actual
    with conexion:
        buffer = ""
        while True:
            datos = conexion.recv(1024)
            if not datos:
                break
            buffer += datos.decode("utf-8")
            
            # Extraer el mensaje completo usando el delimitador \n
            if "\n" in buffer:
                linea, buffer = buffer.split("\n", 1)
                
                if linea.startswith("TURNO>"):
                    apodo = linea.split(">")[1]
                    
                    # Sección crítica: proteger el incremento del contador
                    with lock_turno:
                        turno_actual += 1
                        turno_asignado = turno_actual
                    
                    # Responder al cliente
                    respuesta = f"turno>{turno_asignado}\n"
                    conexion.sendall(respuesta.encode("utf-8"))
                    print(f"Turno {turno_asignado} asignado a '{apodo}' desde {direccion}")
                
                # Para esta práctica, cerramos la conexión tras dar el turno
                break

def servidor_tcp():
    """Configura y ejecuta el servidor TCP en el puerto 5000."""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", 5000))
    servidor.listen()
    print("Servidor TCP (Turnos) escuchando en el puerto 5000")
    
    while True:
        conexion, direccion = servidor.accept()
        # Un hilo por cliente conectado
        hilo = threading.Thread(target=atender_cliente_tcp, args=(conexion, direccion), daemon=True)
        hilo.start()

def servidor_udp():
    """Configura y ejecuta el servidor UDP en el puerto 5001."""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind(("0.0.0.0", 5001))
    print("Servidor UDP (Consultas) escuchando en el puerto 5001")
    
    while True:
        datos, direccion = servidor.recvfrom(1024)
        mensaje = datos.decode("utf-8").strip()
        
        if mensaje == "CUANTOS":
            # Lectura segura de la variable compartida
            with lock_turno:
                total = turno_actual
            
            respuesta = f"van>{total}\n"
            servidor.sendto(respuesta.encode("utf-8"), direccion)

def main():
    # Lanzar el servidor UDP en su propio hilo
    hilo_udp = threading.Thread(target=servidor_udp, daemon=True)
    hilo_udp.start()
    
    # El hilo principal se encarga del servidor TCP
    servidor_tcp()

if __name__ == "__main__":
    main()