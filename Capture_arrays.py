import time
import datetime
import threading

# Se crea un arreglo vacío para almacenar los datos
datos = []

sensor = 3

def insertar_datos(id, eth_mac, date, sensor):
    try:
        now = datetime.datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        pulsos = (id, date_time, date, eth_mac, sensor)
        datos.append(pulsos)
        print("Datos insertados en el arreglo.")
    except Exception as e:
        print("Error al insertar datos en el arreglo:", e)

def limpiar_datos():
    while True:
        time.sleep(10)  # Espera 10 segundos
        if datos:
            print("\nDatos a ser borrados del arreglo:")
            for dato in datos:
                print(dato)
            datos.clear()
            print("Datos borrados del arreglo.")

# Comienza el hilo para limpiar los datos cada diez segundos
thread = threading.Thread(target=limpiar_datos)
thread.daemon = True  # Permite que el hilo se detenga cuando se cierre el programa principal
thread.start()

# Comienza el ciclo, se insertan los datos en el arreglo
eth_mac = "1d:74:50:a:61:a8"

while True:
    id = input("Escanea el código de barras (o introduce 'exit' para salir): ")
    if id.lower() == "exit":
        break

    date = int(time.time() * 1000)
    insertar_datos(id, eth_mac, date, sensor)

# No es necesario cerrar el hilo explícitamente, ya que es un hilo demonio
