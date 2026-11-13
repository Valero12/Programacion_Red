import socket
import threading

def atender_cliente(conexion, direccion):
    """Atiende a un cliente de forma aislada manteniendo un contador de mensajes propio."""
    try:
        with conexion:
            buffer = ""
            contador_mensajes = 0
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    break
                buffer += datos.decode("utf-8")
                
                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)
                    contador_mensajes += 1
                    respuesta = f"{contador_mensajes}>{linea}\n"
                    conexion.sendall(respuesta.encode("utf-8"))
    except ConnectionResetError:
        print(f"El cliente {direccion} se desconectó abruptamente.")
    except BrokenPipeError:
        print(f"No se pudo enviar respuesta al cliente {direccion} (Broken Pipe).")
    finally:
        print(f"Conexión cerrada para el cliente {direccion}.")

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", 5000))
    servidor.listen()
    print("Servidor de eco con contador por cliente escuchando en el puerto 5000...")
    
    while True:
        conexion, direccion = servidor.accept()
        hilo = threading.Thread(target=atender_cliente, args=(conexion, direccion), daemon=True)
        hilo.start()

if __name__ == "__main__":
    main()