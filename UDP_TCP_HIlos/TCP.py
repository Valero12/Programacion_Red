import socket
import sys

def main():
    # Permite pasar el apodo como argumento en la terminal
    apodo = sys.argv[1] if len(sys.argv) > 1 else "Estudiante"
    
    try:
        with socket.create_connection(("127.0.0.1", 5000)) as conexion:
            # Protocolo TCP: mensaje termina con \n
            mensaje = f"TURNO>{apodo}\n"
            conexion.sendall(mensaje.encode("utf-8"))
            
            # Recibir la respuesta
            respuesta = conexion.recv(1024).decode("utf-8").strip()
            print(f"Servidor responde: {respuesta}")
            
    except ConnectionRefusedError:
        print("Error: El servidor TCP no está activo en el puerto 5000.")

if __name__ == "__main__":
    main()