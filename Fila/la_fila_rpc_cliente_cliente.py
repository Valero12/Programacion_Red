import xmlrpc.client

def main():
    # Se crea el stub apuntando a la URL del servidor XML-RPC (que viaja sobre HTTP)[cite: 12, 13, 14]
    print("Conectando con el servidor RPC de 'LA FILA'...")
    servidor = xmlrpc.client.ServerProxy("http://localhost:5000")
    
    # Petición de datos al usuario por teclado
    apodo = input("Ingrese su apodo para la fila: ").strip()
    if not apodo:
        apodo = "Invitado"
        
    try:
        print("\nEnviando peticiones remotas al servidor...")
        
        # Llamadas a procedimientos remotos como si fueran funciones locales[cite: 11, 14]
        mi_turno = servidor.tomar_turno(apodo)
        total_acumulado = servidor.cuantos_van()
        
        # Despliegue de resultados en consola
        print("\n=== RESPUESTA DEL SERVIDOR RPC ===")
        print(f"¡Hola, {apodo}! Tu número de turno asignado es: [{mi_turno}]")
        print(f"Total de personas formadas hasta ahora: {total_acumulado}")
        print("===================================")
        
    except Exception as e:
        print(f"Ocurrió un error al realizar la llamada RPC: {e}")

if __name__ == "__main__":
    main()