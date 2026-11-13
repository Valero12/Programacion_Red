import threading
import time

def saludar(nombre, veces):
    """Función ejecutada por cada hilo que realiza una serie de saludos con pausa."""
    for i in range(1, veces + 1):
        print(f"Hilo [{nombre}]: Saludo {i}")
        time.sleep(0.5)
    print(f"-> Hilo [{nombre}] ha terminado.")

def main():
    tareas = [("Ana", 3), ("Beto", 5), ("Cora", 2)]
    hilos = []
    
    # Creación y arranque de los hilos
    for nombre, veces in tareas:
        hilo = threading.Thread(
            target=saludar, 
            args=(nombre, veces), 
            name=f"Hilo-{nombre}"
        )
        hilos.append(hilo)
        hilo.start()
        
    # Esperar a que todos los hilos terminen con join()
    for hilo in hilos:
        hilo.join()
        
    print("¡Todos los hilos han finalizado con éxito! Mensaje final del programa principal.")

if __name__ == "__main__":
    main()