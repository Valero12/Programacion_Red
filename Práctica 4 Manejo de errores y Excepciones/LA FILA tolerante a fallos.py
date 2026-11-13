import socket
import threading

contador_turnos = 0
lock_contador = threading.Lock()

def atender_cliente(conexion, direccion):
    global contador_turnos
    try:
        with conexion:
            buffer = ""
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    break
                
                # Manejo de excepciones ante codificación incorrecta
                try:
                    texto = datos.decode("utf-8")
                except UnicodeDecodeError:
                    print(f"[{direccion}] Advertencia: Se recibieron bytes que no son UTF-8 válido.")
                    conexion.sendall("ERROR>Codificacion UTF-8 no soportada\n".encode("utf-8"))
                    continue
                
                buffer += texto
                
                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)
                    linea = linea.strip()
                    
                    # Validación estricta del protocolo
                    if linea.startswith("TURNO>"):
                        apodo = linea[6:]
                        with lock_contador:
                            contador_turnos += 1
                            turno_actual = contador_turnos
                        
                        respuesta = f"SU_TURNO>{turno_actual}:{apodo}\n"
                        conexion.sendall(respuesta.encode("utf-8"))
                        print(f"[{direccion}] Turno asignado #{turno_actual} para '{apodo}'")
                    else:
                        print(f"[{direccion}] Protocolo violado por mensaje: '{linea}'")
                        conexion.sendall("ERROR>Formato invalido. Use TURNO>apodo\n".encode("utf-8"))
                        
    except ConnectionResetError:
        print(f"El cliente {direccion} cerró la conexión abruptamente.")
    except BrokenPipeError:
        print(f"Error de envío: Canal roto con el cliente {direccion}.")
    finally:
        print(f"Conexión finalizada y recursos liberados para {direccion}.")

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", 5000))
    servidor.listen()
    print("Servidor 'LA FILA' tolerante a fallos escuchando en el puerto 5000...")
    
    while True:
        conexion, direccion = servidor.accept()
        hilo = threading.Thread(target=atender_cliente, args=(conexion, direccion), daemon=True)
        hilo.start()

if __name__ == "__main__":
    main()