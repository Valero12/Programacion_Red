import socket
import sys

def main():
    ip = input("Ingrese la IP o hostname del servidor: ").strip()
    puerto = 5000
    
    try:
        print(f"Intentando conectar a {ip}:{puerto}...")
        conexion = socket.create_connection((ip, puerto), timeout=5)
    except socket.gaierror:
        print(f"Error: No se pudo resolver el nombre o la dirección IP '{ip}' es inválida.")
        sys.exit(1)
    except ConnectionRefusedError:
        print("Error: El servidor no está disponible (conexión rechazada).")
        sys.exit(1)
    except TimeoutError:
        print("Error: El servidor tardó demasiado en responder (Timeout).")
        sys.exit(1)
    except OSError as e:
        print(f"Error de red inesperado al conectar: {e}")
        sys.exit(1)
        
    try:
        with conexion:
            mensaje = "hola\n"
            conexion.sendall(mensaje.encode("utf-8"))
            respuesta = conexion.recv(1024).decode("utf-8").strip()
            print(f"Servidor responde: {respuesta}")
    except ConnectionResetError:
        print("Error: El servidor cerró la conexión inesperadamente durante la comunicación.")
        sys.exit(1)
    except BrokenPipeError:
        print("Error: Se intentó escribir en una tubería rota (Broken Pipe).")
        sys.exit(1)
    except Exception as e:
        print(f"Error imprevisto: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()