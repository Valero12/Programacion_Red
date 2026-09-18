import socket
#Crear socket UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#No requiere connect(), se envia directamente a la dirección destino
cliente.sendto("Hola Servidor UDP".encode('utf-8'), ('localhost', 5001))

respuesta,servidor_addr = cliente.recvfrom(1024)
print(f"Respuesta del servidor: {respuesta.decode('utf-8')}")

cliente.close()
