import socket
#Crear socket UDP(SOCK_DGRAM)
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(('localhost', 5001))

print("Servidor UDP listo para recibir datos...")

#REcibe el mensaje y la direccion del remitente al mismo tiempo
mensaje,direccion = servidor.recvfrom(1024)
print(f"Mensaje recibido de {direccion}:{mensaje.decode('utf-8')}")
servidor.sendto("Respuesta rápida (UDP)".encode('utf-8'), direccion)

servidor.close()
