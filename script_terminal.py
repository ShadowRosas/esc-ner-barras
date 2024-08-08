import subprocess
import requests
import time
from datetime import datetime

def ejecutar_comando(comando):
    subprocess.Popen(comando, shell=True)

# Esperar 30 segundos antes de ejecutar el resto del script
time.sleep(1)

# Obtener la hora actual de Tijuana desde una API pública
response = requests.get("http://worldtimeapi.org/api/timezone/America/Tijuana")
if response.status_code == 200:
    data = response.json()
    tijuana_datetime_str = data["datetime"]
    # Formatear la hora y fecha obtenida en el formato requerido por el comando `date`
    tijuana_datetime = datetime.fromisoformat(tijuana_datetime_str.replace("Z", "+00:00"))
    formatted_date = tijuana_datetime.strftime("%m%d%H%M%Y.%S")
    
    # Comando para establecer la fecha y hora en la Raspberry Pi
    command = f"sudo date {formatted_date}"
    print(f"Ejecutando comando: {command}")
    ejecutar_comando(command)

else:
    print("No se pudo obtener la hora actual de Tijuana.")
