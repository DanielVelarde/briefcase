import psycopg2
import csv
from datetime import datetime

# Conectar a la base de datos PostgreSQL
def connect_to_db():
    conn = psycopg2.connect(
        dbname="Binance",  # Reemplaza con el nombre de tu base de datos
        user="ero",          # Reemplaza con tu usuario
        password="6962277",   # Reemplaza con tu contraseña
        host="localhost",           # Cambia si tu base de datos no está en localhost
        port="5432"                 # Cambia si tu puerto no es 5432
    )
    return conn

# Función para insertar las criptomonedas en la tabla 'cryptocurrencies'
def insert_cryptocurrencies(conn, cryptocurrencies):
    with conn.cursor() as cursor:
        for currency in cryptocurrencies:
            cursor.execute("""
                INSERT INTO cryptocurrencies (name)
                VALUES (%s) ON CONFLICT (name) DO NOTHING;
            """, (currency,))
        conn.commit()

# Función para insertar los pares en las tablas correspondientes (USDT, BTC, ETH)
def insert_pairs(conn, pair_data, pair_type):
    with conn.cursor() as cursor:
        for row in pair_data:
            base_currency = row['base_currency']
            quote_currency = row['quote_currency']

            # Asegurarse de que las criptomonedas existen en la tabla 'cryptocurrencies'
            cursor.execute("""
                INSERT INTO cryptocurrencies (name)
                VALUES (%s) ON CONFLICT (name) DO NOTHING;
            """, (base_currency,))
            cursor.execute("""
                INSERT INTO cryptocurrencies (name)
                VALUES (%s) ON CONFLICT (name) DO NOTHING;
            """, (quote_currency,))

            # Obtener los ids de las criptomonedas
            cursor.execute("SELECT id FROM cryptocurrencies WHERE name = %s;", (base_currency,))
            base_currency_id = cursor.fetchone()[0]
            cursor.execute("SELECT id FROM cryptocurrencies WHERE name = %s;", (quote_currency,))
            quote_currency_id = cursor.fetchone()[0]

            # Insertar el par en la tabla correspondiente
            if pair_type == 'usdt':
                cursor.execute("""
                    INSERT INTO usdt_pairs (base_currency_id, quote_currency_id)
                    VALUES (%s, %s) ON CONFLICT (base_currency_id, quote_currency_id) DO NOTHING;
                """, (base_currency_id, quote_currency_id))
            elif pair_type == 'btc':
                cursor.execute("""
                    INSERT INTO btc_pairs (base_currency_id, quote_currency_id)
                    VALUES (%s, %s) ON CONFLICT (base_currency_id, quote_currency_id) DO NOTHING;
                """, (base_currency_id, quote_currency_id))
            elif pair_type == 'eth':
                cursor.execute("""
                    INSERT INTO eth_pairs (base_currency_id, quote_currency_id)
                    VALUES (%s, %s) ON CONFLICT (base_currency_id, quote_currency_id) DO NOTHING;
                """, (base_currency_id, quote_currency_id))

        conn.commit()

# Función para insertar datos históricos en las tablas correspondientes
def insert_historical_data(conn, pair_data, pair_type):
    with conn.cursor() as cursor:
        for row in pair_data:
            pair = row['pair']
            timestamp = row['timestamp']
            open_price = row['open']
            high_price = row['high']
            low_price = row['low']
            close_price = row['close']
            volume = row['volume']

            # Obtener el id del par correspondiente
            cursor.execute(f"SELECT id FROM {pair_type}_pairs WHERE base_currency_id = (SELECT id FROM cryptocurrencies WHERE name = %s) AND quote_currency_id = (SELECT id FROM cryptocurrencies WHERE name = %s);", (pair.split('/')[0], pair.split('/')[1]))
            pair_id = cursor.fetchone()[0]

            # Insertar los datos históricos en la tabla correspondiente
            if pair_type == 'usdt':
                cursor.execute("""
                    INSERT INTO usdt_data (pair_id, timestamp, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (pair_id, timestamp, open_price, high_price, low_price, close_price, volume))
            elif pair_type == 'btc':
                cursor.execute("""
                    INSERT INTO btc_data (pair_id, timestamp, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (pair_id, timestamp, open_price, high_price, low_price, close_price, volume))
            elif pair_type == 'eth':
                cursor.execute("""
                    INSERT INTO eth_data (pair_id, timestamp, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (pair_id, timestamp, open_price, high_price, low_price, close_price, volume))

        conn.commit()

# Función principal para cargar el archivo CSV y procesarlo
def load_data_to_db(csv_file, conn):
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        # Agrupar las criptomonedas y los pares de datos por tipo (USDT, BTC, ETH)
        cryptocurrencies = set()
        usdt_data = []
        btc_data = []
        eth_data = []

        for row in reader:
            pair = row['Symbol']
            pair_type = pair.split('/')[1].lower()  # Determina el tipo de par (USDT, BTC, ETH)
            data = {
                'pair': pair,
                'timestamp': datetime.utcfromtimestamp(int(row['Timestamp']) / 1000),  # Convertir el timestamp en milisegundos
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': float(row['Volume']),
                'base_currency': pair.split('/')[0],
                'quote_currency': pair.split('/')[1]
            }

            cryptocurrencies.add(data['base_currency'])
            cryptocurrencies.add(data['quote_currency'])

            if pair_type == 'usdt':
                usdt_data.append(data)
            elif pair_type == 'btc':
                btc_data.append(data)
            elif pair_type == 'eth':
                eth_data.append(data)

        # Insertar las criptomonedas en la tabla 'cryptocurrencies'
        insert_cryptocurrencies(conn, cryptocurrencies)

        # Insertar pares en las tablas correspondientes
        insert_pairs(conn, usdt_data, 'usdt')
        insert_pairs(conn, btc_data, 'btc')
        insert_pairs(conn, eth_data, 'eth')

        # Insertar los datos históricos en las tablas correspondientes
        insert_historical_data(conn, usdt_data, 'usdt')
        insert_historical_data(conn, btc_data, 'btc')
        insert_historical_data(conn, eth_data, 'eth')

# Ejecutar el proceso
if __name__ == "__main__":
    conn = connect_to_db()
    try:
        load_data_to_db('processed_cryptos_data.csv', conn)
        print("Datos cargados exitosamente.")
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
    finally:
        conn.close()
