import socket
#Crear socket TCP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost',5000)) #Establece la conexion primero

cliente.send("Hola servidor TCP".encode('utf-8'))
respuesta = cliente.recv(1024).decode('utf-8')
print(f"Respuesta del servidor:{respuesta}")

cliente.close()
