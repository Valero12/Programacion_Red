import socket
import time

def consultar(servidor, mensaje, reintentos=3):
    """Envía una consulta UDP y reintenta con espera exponencial (1, 2, 4 s) si no hay respuesta."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        cliente.settimeout(2)
        for intento in range(1, reintentos + 1):
            try:
                print(f"Enviando datagrama (Intento {intento}/{reintentos})...")
                cliente.sendto((mensaje + "\n").encode("utf-8"), servidor)
                datos, _ = cliente.recvfrom(1024)
                return datos.decode("utf-8").strip()
            except TimeoutError:
                espera = 2 ** (intento - 1)  # 2^0 = 1, 2^1 = 2, 2^2 = 4
                print(f"Intento {intento} sin respuesta. Reintentando en {espera} segundos...")
                if intento < reintentos:
                    time.sleep(espera)
        return None

def main():
    servidor_dir = ("127.0.0.1", 5001)
    respuesta = consultar(servidor_dir, "CUANTOS", reintentos=3)
    if respuesta:
        print(f"Resultado exitoso: {respuesta}")
    else:
        print("El servidor no respondió tras agotar los reintentos.")

if __name__ == "__main__":
    main()