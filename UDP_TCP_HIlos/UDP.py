import socket

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        # Si no hay respuesta en 3 segundos, lanza TimeoutError
        cliente.settimeout(3)
        
        try:
            # UDP: un datagrama equivale a un mensaje completo
            cliente.sendto("CUANTOS".encode("utf-8"), ("127.0.0.1", 5001))
            
            # Esperar la respuesta
            datos, _ = cliente.recvfrom(1024)
            print(f"Servidor responde: {datos.decode('utf-8').strip()}")
            
        except socket.timeout:
            print("Error: Se agotó el tiempo de espera. El servidor UDP no responde.")

if __name__ == "__main__":
    main()