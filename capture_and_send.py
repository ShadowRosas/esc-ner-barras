import time
import datetime
import requests

sensor = 999

# URL del servidor donde se enviarán los datos
url = 'https://amphenol.goandsee.co/api/v3/oee'

def insertar_datos(id, eth_mac, date, sensor):
    try:
        now = datetime.datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        data = {
            'id': id,
            'date_time': date_time,
            'date': date,
            'eth_mac': eth_mac,
            'sensor': sensor
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Datos enviados al servidor.")
        else:
            print("Error al enviar datos al servidor:", response.status_code)
    except Exception as e:
        print("Error al enviar datos al servidor:", e)

# Comienza el ciclo, se envían los datos al servidor
eth_mac = "123456789"

while True:
    id = input("Escanea el código de barras (o introduce 'exit' para salir): ")
    if id.lower() == "exit":
        break

    date = int(time.time() * 1000)
    insertar_datos(id, eth_mac, date, sensor)
