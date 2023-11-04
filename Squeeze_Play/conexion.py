import psycopg2
import requests
import pandas as pd
from sqlalchemy import create_engine

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

def obtener_datos_historicos(interval):
    conn, cursor = establecer_conexion()
    if conn is not None and cursor is not None:
        cursor.execute("SELECT currency FROM coin_list")
        coins = cursor.fetchall()
        conn.close()

        historical_data = []

        for coin in coins:
            currency = coin[0]
            symbol = f"{currency}-USDT"

            url = f"https://api.kucoin.com/api/v1/market/candles?type={interval}&symbol={symbol}"

            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if data["code"] == "200000":
                        historical_prices = data["data"]
                        if historical_prices:
                            for price_data in historical_prices:
                                price_data.append(currency)  # Agregar una columna para la moneda correspondiente
                                historical_data.append(price_data)
                        else:
                            print(f"No se encontraron datos históricos para {currency}.")
                    else:
                        print(f"No se encontraron datos históricos para {currency}")
                else:
                    print(f"Error al obtener datos históricos para {currency}: Código de estado {response.status_code}")
            except Exception as e:
                print(f"Error de conexión para {currency}: {e}")

        return historical_data
    else:
        return []

def guardar_datos_historicos_en_csv(historical_data, interval):
    columns = ["timestamp", "open", "high", "low", "close", "volume", "assetvolume", "currency"]
    historical_df = pd.DataFrame(historical_data, columns=columns)

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

    historical_data_df['timestamp'] = pd.to_datetime(historical_data_df['timestamp'])
    historical_data_df.to_sql(f'/home/erosennin/briefcase/Squeeze_Play/historical_data_{interval}', engine, if_exists="append", index=False)

def main():
    conn, cursor = establecer_conexion()

    if conn is not None and cursor is not None:
        currencies = obtener_lista_monedas()
        guardar_monedas_en_db(conn, cursor, currencies)

        intervals = ["1day", "1week", "1month"]
        for interval in intervals:
            historical_data = obtener_datos_historicos(interval)
            if historical_data:
                csv_filename = guardar_datos_historicos_en_csv(historical_data, interval)
                guardar_datos_historicos_en_db(conn, cursor, csv_filename, interval)

        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
