from xmlrpc.server import SimpleXMLRPCServer
import threading

# Variables compartidas protegidas por un Lock para concurrencia con múltiples clientes
contador_turnos = 0
lock_turnos = threading.Lock()

def tomar_turno(apodo):
    """Asigna un número de turno consecutivo y seguro ante múltiples hilos."""
    global contador_turnos
    with lock_turnos:
        contador_turnos += 1
        turno_actual = contador_turnos
    print(f"[SERVIDOR] Turno asignado #{turno_actual} para el apodo: '{apodo}'")
    return turno_actual

def cuantos_van():
    """Devuelve el total de turnos emitidos hasta el momento."""
    with lock_turnos:
        actual = contador_turnos
    print(f"[SERVIDOR] Se consultó el total de turnos. Van: {actual}")
    return actual

def main():
    # Inicializa el servidor XML-RPC en localhost en el puerto 5000
    # allow_none=True permite manejar valores nulos si fuera necesario
    servidor = SimpleXMLRPCServer(("localhost", 5000), allow_none=True)
    
    # Registro de funciones públicas accesibles por los clientes
    servidor.register_function(tomar_turno, "tomar_turno")
    servidor.register_function(cuantos_van, "cuantos_van")
    
    print("Servidor RPC de 'LA FILA' escuchando en el puerto 5000...")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido de forma ordenada.")

if __name__ == "__main__":
    main()