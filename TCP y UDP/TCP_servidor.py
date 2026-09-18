import socket
#Crear socket TCP (Sock_stream)
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('localhost', 5000))
servidor.listen(1)

print("Servidor TCP esperando conexión...")
conexion, direccion = servidor.accept() #Acepta la conexión del cliente
print("Conectado con:{direccion}")

mensaje = conexion.recv(1024).decode("utf-8")
print(f"Mensaje recibido:{mensaje}")

conexion.send("Mensaje recibido correctamente (TCP)".enconde("utf-8"))
conexion.close()
servidor.close()

