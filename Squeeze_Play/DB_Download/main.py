from datetime import datetime, timedelta
import os
import database
import crypto_data
import file_operations
from tqdm import tqdm  # Importar tqdm

output_dir = "DB_Download"  # Ruta donde se guardarán los archivos CSV

def main():
    conn, cursor = database.establecer_conexion()

    if conn is not None and cursor is not None:
        # Cargar la tabla de monedas en la base de datos
        currencies = crypto_data.obtener_lista_monedas()
        database.guardar_monedas_en_db(conn, cursor, currencies)

        # Proceder a obtener datos históricos
        coins = [{"currency": currency["currency"]} for currency in currencies]

        intervals = ["day", "week", "month"]

        for interval in intervals:
            last_date = database.obtener_ultima_fecha_descarga(conn, interval)
            today = datetime.now().date()

            if interval == "week":
                interval_days = 7
            elif interval == "month":
                interval_days = 30
            else:
                interval_days = 1

            if last_date is None or (today - last_date).days >= interval_days:
                historical_data = crypto_data.obtener_datos_historicos(interval, coins)
                if historical_data:
                    # Guardar datos históricos en el directorio actual sin output_dir
                    csv_filename = file_operations.guardar_datos_historicos_en_csv(historical_data, interval)
                    database.guardar_datos_historicos_en_db(conn, cursor, csv_filename, interval)
                else:
                    print(f"No se pudieron obtener datos para {interval}.")
            else:
                print(f"No se requiere descargar datos para {interval} hoy.")

        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
