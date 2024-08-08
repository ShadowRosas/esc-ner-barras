import time
import datetime
import threading
import requests
from pynput import keyboard

# Se crea un arreglo vacío para almacenar los datos
datos = []

# Definir el punto final de la API
API_ENDPOINT = 'https://amphenol.goandsee.co/api/v3/oee'

sensor = 999

def insertar_datos(id, eth_mac, date, sensor):
    try:
        now = datetime.datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        pulsos = (id, date_time, date, eth_mac, sensor)
        
        # Verificar si el código de barras ya está en el arreglo
        if not any(dato[0] == id for dato in datos):
            datos.append(pulsos)
            print("Datos insertados en el arreglo.")
        else:
            print("El código de barras ya existe en el arreglo, no se insertará.")
    except Exception as e:
        print("Error al insertar datos en el arreglo:", e)

def limpiar_datos():
    while True:
        time.sleep(10)  # Espera 10 segundos
        try:
            if datos:
                # Convertir las filas en un formato aceptable para la API (por ejemplo, lista de diccionarios)
                datos_api = [{'id': pulso[0], 'date_time': pulso[1], 'date': pulso[2], 'eth_mac': pulso[3], 'sensor': pulso[4]} for pulso in datos]
                response = requests.post(url=API_ENDPOINT, json=datos_api)
                response.raise_for_status()
                print("Datos subidos exitosamente. Código de estado:", response.status_code)
                datos.clear()
            else:
                print("No hay datos para enviar.")
        except requests.exceptions.RequestException as e:
            print("Error al enviar datos a la API:", e)

# Comienza el hilo para limpiar los datos cada diez segundos
thread = threading.Thread(target=limpiar_datos)
thread.daemon = True  # Permite que el hilo se detenga cuando se cierre el programa principal
thread.start()

# Comienza la detección del escáner de código de barras
print("Esperando datos del escáner...")

barcode = ''
def on_press(key):
    global barcode
    try:
        if key == keyboard.Key.enter:
            if barcode:
                date = int(time.time() * 1000)
                insertar_datos(barcode, "123456789", date, sensor)
                barcode = ''  # Restablecer el valor del código de barras
        else:
            barcode += key.char
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        return False

# Configurar los listeners del teclado
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
