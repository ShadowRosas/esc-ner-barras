import pandas as pd
import datetime
import requests
import schedule
import time
import pytz

def enviar_datos():
    archivo_excel = 'Código/agosto.xlsm'
    url = 'https://amphenol.goandsee.co/api/v3/oee'
    
    try:
        xl = pd.ExcelFile(archivo_excel)
        hojas = xl.sheet_names  # Obtiene una lista de todas las hojas en el archivo

        for nombre_hoja in hojas:
            try:
                df = pd.read_excel(xl, sheet_name=nombre_hoja)
                print(f"Procesando hoja: {nombre_hoja} con {df.shape[0]} filas y {df.shape[1]} columnas.")

                if df.shape[1] < 8:
                    print("La hoja no tiene suficientes columnas para procesar.")
                    continue

                qty_column = pd.to_numeric(df.iloc[:, 5], errors='coerce')
                tijuana_tz = pytz.timezone('America/Tijuana')
                hour_column = pd.to_datetime(df.iloc[:, 7], errors='coerce', format='%H:%M:%S')
                hour_column = hour_column.dt.tz_localize(tijuana_tz, ambiguous='NaT', nonexistent='shift_forward')

                pulsos_simplificados = []
                for idx, (qty, hour) in enumerate(zip(qty_column, hour_column)):
                    if pd.notna(qty) and qty > 0:
                        initial_time = hour.replace(minute=0, second=0, microsecond=0)
                        total_minutes = hour.minute + hour.second / 60
                        interval_minutes = total_minutes / (qty - 1) if qty > 1 else total_minutes
                        for i in range(int(qty)):
                            next_time = initial_time + datetime.timedelta(minutes=interval_minutes * i)
                            pulsos_simplificados.append({
                                'datetime': next_time.strftime('%H:%M:%S'),
                                'date': int(next_time.timestamp() * 1000),
                                'eth_mac': "123456789",
                                'sensor': 999,
                            })

                for pulse_data in pulsos_simplificados:
                    response = requests.post(url, json=pulse_data)
                    if response.status_code != 200:
                        print("Error al enviar datos al servidor:", response.status_code)

                print(f"Datos de la hoja {nombre_hoja} enviados con éxito.")

            except Exception as e:
                print(f"Error procesando la hoja {nombre_hoja}: {e}")
                continue

    except Exception as e:
        print(f"Error al abrir el archivo Excel: {e}")

def job():
    print("Iniciando el proceso de envío de datos...")
    enviar_datos()

# Programa el trabajo para que se ejecute cada hora en punto
schedule.every().hour.at(":47").do(job)

if __name__ == "__main__":
    print("El script de envío de datos ha sido iniciado y está programado para ejecutarse cada hora en punto.")
    while True:
        schedule.run_pending()
        time.sleep(1)
