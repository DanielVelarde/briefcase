import psycopg2
import requests
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
from datetime import datetime, timedelta, timezone

# Configuración de la base de datos
dbname = "kucoin"
user = "postgres"
password = "6962277"
host = "localhost"
port = "5432"

def establecer_conexion():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cursor = conn.cursor()
        print("Conexión exitosa")
        return conn, cursor
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None, None

def crear_tablas_si_no_existen():
    conn, cursor = establecer_conexion()
    if conn is not None and cursor is not None:
        intervals = ["1day", "1week", "1month"]
        for interval in intervals:
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS historical_data_{interval} (
                timestamp TIMESTAMP,
                open NUMERIC,
                low NUMERIC,
                high NUMERIC,
                close NUMERIC,
                volume NUMERIC,
                assetvolume NUMERIC,
                currency VARCHAR
            );
            """
            cursor.execute(create_table_query)
            conn.commit()
        cursor.close()
        conn.close()

def obtener_lista_monedas():
    api_url = 'https://api.kucoin.com/api/v3/currencies'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        currencies = data.get('data', [])
        return currencies
    else:
        print("Error al obtener la lista de monedas")
        return []

def guardar_monedas_en_db(conn, cursor, currencies):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coin_list (
                currency VARCHAR PRIMARY KEY,
                name VARCHAR,
                fullName VARCHAR,
                precision INT,
                isMarginEnabled BOOLEAN,
                isDebitEnabled BOOLEAN
            )
        """)
        conn.commit()
        print("Tabla 'coin_list' creada o ya existe")

        for currency in currencies:
            cursor.execute("""
                INSERT INTO coin_list (currency, name, fullName, precision, isMarginEnabled, isDebitEnabled)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (currency) DO NOTHING
            """, (currency['currency'], currency['name'], currency['fullName'],
                  currency['precision'], currency['isMarginEnabled'], currency['isDebitEnabled']))

        conn.commit()
        print("Datos insertados exitosamente")

    except Exception as e:
        conn.rollback()
        print(f"Error al crear o insertar datos en la tabla: {e}")

def obtener_ultima_fecha(interval):
    conn, cursor = establecer_conexion()
    if conn is not None and cursor is not None:
        cursor.execute(f"SELECT MAX(EXTRACT(epoch FROM timestamp)::float) FROM historical_data_{interval}")
        last_date_timestamp = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        last_date = datetime.utcfromtimestamp(last_date_timestamp).replace(tzinfo=timezone.utc) if last_date_timestamp else None

        if last_date:
            current_date = datetime.now(timezone.utc)
            if interval == "1week" and (current_date - last_date).days < 7:
                print(f"No han pasado suficientes días para el intervalo {interval}. No se requiere actualizar.")
                return last_date, True

            if last_date.date() >= current_date.date():
                print(f"Los datos están actualizados para el intervalo {interval}. No se requiere actualizar.")
                return last_date, True

        print(f"Última fecha en la base de datos para el intervalo {interval}: {last_date}")
        return last_date, False  # Cambiamos True a False para indicar que no hay datos en la base de datos

    else:
        print(f"No se pudo obtener la última fecha para el intervalo {interval}")
        return None, False

def obtener_nueva_data(interval, start_date, end_date):
    conn, cursor = establecer_conexion()
    if conn is not None and cursor is not None:
        cursor.execute("SELECT currency FROM coin_list")
        coins = cursor.fetchall()
        conn.close()

        historical_data = []

        print(f"Descargando datos históricos ({interval}) desde {start_date} hasta {end_date}")

        with tqdm(coins, position=0, leave=True, ncols=100, desc=f"Descargando datos históricos ({interval})") as pbar:
            for coin in coins:
                currency = coin[0]
                symbol = f"{currency}-USDT"
                url = f"https://api.kucoin.com/api/v1/market/candles?type={interval}&symbol={symbol}&startAt={start_date}&endAt={end_date}"

                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        #print(f"Respuesta de la API para {currency}: {data}")  # Agrega esta línea para imprimir la respuesta de la API
                        if data["code"] == "200000":
                            historical_prices = data.get("data", [])  # Obtener la lista de precios, o una lista vacía si no hay datos
                            for price_data in historical_prices:
                                price_data.append(currency)  # Agregar una columna para la moneda correspondiente
                                historical_data.append(price_data)
                            continue
                    else:
                        continue
                except Exception as e:
                    print(f"Error de conexión para {currency}: {e}")
                    continue

                pbar.update(1)

        #print(f"Datos obtenidos para {interval}: {historical_data}")
        return historical_data
    
def guardar_datos_historicos_en_csv(historical_data, interval):
    columns = ["timestamp", "open", "high", "low", "close", "volume", "assetvolume", "currency"]

    # Modificamos la forma en que se manejan las fechas
    for data_point in historical_data:
        data_point[0] = datetime.utcfromtimestamp(int(data_point[0])).strftime('%Y-%m-%d %H:%M:%S')

    historical_df = pd.DataFrame(historical_data, columns=columns)

    # Cambiamos los nombres de las columnas sin afectar los datos
    historical_df = historical_df.rename(columns={'high': 'low', 'low': 'high'})

    csv_filename = f"/home/erosennin/briefcase/Squeeze_Play/historical_data_{interval}.csv"
    historical_df.to_csv(csv_filename, index=False)

    return csv_filename


def guardar_datos_historicos_en_db(conn, cursor, csv_filename, interval):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS historical_data_{interval} (
        timestamp TIMESTAMP,
        open NUMERIC,
        high NUMERIC,
        low NUMERIC,
        close NUMERIC,
        volume NUMERIC,
        assetvolume NUMERIC,
        currency VARCHAR
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}')
    historical_data_df = pd.read_csv(csv_filename)
    print("domo")
    try:
        historical_data_df['timestamp'] = pd.to_datetime(historical_data_df['timestamp'])
        historical_data_df.to_sql(f'historical_data_{interval}', engine, if_exists="append", index=False)
        print(f"Datos cargados exitosamente en la base de datos para el intervalo {interval}")
    except Exception as e:
        print(f"Error al cargar datos en la base de datos: {e}")

def main():
    crear_tablas_si_no_existen()
    conn, cursor = establecer_conexion()

    if conn is not None and cursor is not None:
        currencies = obtener_lista_monedas()
        guardar_monedas_en_db(conn, cursor, currencies)

        intervals = ["1day", "1week"]
        for interval in intervals:
            last_date, database_exists = obtener_ultima_fecha(interval)
            current_date = datetime.now()

            if database_exists and last_date is not None:
                print(f"Última fecha convertida a timestamp: {last_date}")
                if interval == "1day":
                    if isinstance(last_date, datetime):
                        start_date_timestamp = int(last_date.timestamp()) + 86400  # Agregar un día en segundos
                        end_date_timestamp = int(current_date.timestamp())
                        historical_data = obtener_nueva_data(interval, start_date_timestamp, end_date_timestamp)

                        print(f"Datos históricos descargados:")
                        if historical_data:
                            csv_filename = guardar_datos_historicos_en_csv(historical_data, interval)
                            guardar_datos_historicos_en_db(conn, cursor, csv_filename, interval)
                    else:
                        print(f"Error: el tipo de last_date no es datetime. Tipo actual: {type(last_date)}")
                elif interval == "1week":
                    if isinstance(last_date, datetime):
                        start_date_timestamp = int(last_date.timestamp()) + 7 * 86400  # Agregar una semana en segundos
                        end_date_timestamp = int(current_date.timestamp())
                        historical_data = obtener_nueva_data(interval, start_date_timestamp, end_date_timestamp)

                        print(f"Datos históricos descargados:")
                        if historical_data:
                            csv_filename = guardar_datos_historicos_en_csv(historical_data, interval)
                            guardar_datos_historicos_en_db(conn, cursor, csv_filename, interval)
                    else:
                        print(f"Error: el tipo de last_date no es datetime. Tipo actual: {type(last_date)}")
                else:
                    # Otros intervalos pueden ser manejados de manera similar según sea necesario
                    pass

            elif not database_exists:
                print(f"No hay registros en la tabla para el intervalo {interval}. Descargando todos los datos desde hace 365 días atrás.")
                start_date_timestamp = int(current_date.timestamp()) - 365 * 86400  # Restar 365 días en segundos
                end_date_timestamp = int(current_date.timestamp())
                historical_data = obtener_nueva_data(interval, start_date_timestamp, end_date_timestamp)

                if historical_data:
                    csv_filename = guardar_datos_historicos_en_csv(historical_data, interval)
                    guardar_datos_historicos_en_db(conn, cursor, csv_filename, interval)

        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
