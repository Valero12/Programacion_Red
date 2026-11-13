import socket
import threading
import time

contador_turnos = 0
lock_recursos = threading.Lock()
LOG_FILE = "servidor_errores.log"

def registrar_error(direccion, mensaje_error):
    """Registra de forma segura (concurrente) los errores en archivo de log."""
    marca_tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
    linea_log = f"{marca_tiempo} {direccion} {mensaje_error}\n"
    with lock_recursos:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(linea_log)
    print(f"[LOG ESCRITO] {linea_log.strip()}")

def atender_cliente(conexion, direccion):
    global contador_turnos
    try:
        with conexion:
            buffer = ""
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    break
                
                try:
                    texto = datos.decode("utf-8")
                except UnicodeDecodeError as e:
                    desc = f"UnicodeDecodeError: bytes inválidos ({e})"
                    registrar_error(direccion, desc)
                    conexion.sendall("ERROR>Codificacion invalida\n".encode("utf-8"))
                    continue
                
                buffer += texto
                
                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)
                    linea = linea.strip()
                    
                    if linea.startswith("TURNO>"):
                        apodo = linea[6:]
                        with lock_recursos:
                            contador_turnos += 1
                            turno_actual = contador_turnos
                        
                        respuesta = f"SU_TURNO>{turno_actual}:{apodo}\n"
                        conexion.sendall(respuesta.encode("utf-8"))
                        print(f"[{direccion}] Turno {turno_actual} asignado a {apodo}")
                    else:
                        desc = f"Protocolo violado - mensaje recibido: '{linea}'"
                        registrar_error(direccion, desc)
                        conexion.sendall("ERROR>Formato incorrecto\n".encode("utf-8"))
                        
    except ConnectionResetError:
        registrar_error(direccion, "conexión reiniciada abruptamente por el cliente (ConnectionResetError)")
    except BrokenPipeError:
        registrar_error(direccion, "tubería rota al intentar enviar datos (BrokenPipeError)")
    except Exception as e:
        registrar_error(direccion, f"excepción no controlada: {type(e).__name__} - {e}")
    finally:
        print(f"Conexión cerrada: {direccion}")

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        servidor.bind(("0.0.0.0", 5000))
    except OSError:
        print("El puerto 5000 ya está ocupado por otro proceso.")
        return
    
    servidor.listen()
    print("Servidor 'LA FILA' con registro de errores en archivo escuchando en el puerto 5000...")
    
    while True:
        conexion, direccion = servidor.accept()
        hilo = threading.Thread(target=atender_cliente, args=(conexion, direccion), daemon=True)
        hilo.start()

if __name__ == "__main__":
    main()