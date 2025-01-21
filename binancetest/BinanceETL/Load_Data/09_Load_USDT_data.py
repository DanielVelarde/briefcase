import psycopg2
import csv

def insert_usdt_data_from_csv(csv_file):
    # Establecer conexión a la base de datos
    conn = psycopg2.connect(
        dbname="Binance", user="ero", password="6962277", host="localhost", port="5432"
    )
    cursor = conn.cursor()

    # Abrir el archivo CSV
    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)  # Usar DictReader para facilitar el acceso a las columnas por nombre

        for row in reader:
            symbol = row["Symbol"].strip()  # El símbolo del par (como ETH/USDT)
            timestamp = row["Timestamp"].strip()  # Fecha y hora
            open_price = float(row["Open"].strip())  # Precio de apertura
            high_price = float(row["High"].strip())  # Precio más alto
            low_price = float(row["Low"].strip())  # Precio más bajo
            close_price = float(row["Close"].strip())  # Precio de cierre
            volume = float(row["Volume"].strip())  # Volumen de transacciones
            crypto = row["Crypto"].strip()  # Nombre de la criptomoneda base
            par = row["Par"].strip()  # Criptomoneda de cotización

            # Verificar si el par contiene "USDT" (solo insertar si es un par USDT)
            if "USDT" not in symbol:
                continue  # Saltar este par si no contiene "USDT"

            # Buscar los IDs de base_currency y quote_currency
            cursor.execute("SELECT id FROM cryptocurrencies WHERE UPPER(name) = %s", (crypto.upper(),))
            base_id = cursor.fetchone()
            cursor.execute("SELECT id FROM cryptocurrencies WHERE UPPER(name) = %s", (par.upper(),))
            quote_id = cursor.fetchone()

            # Si no se encuentran las criptos en la tabla, saltar este par
            if base_id is None or quote_id is None:
                print(f"El par {crypto}/{par} no está en cryptocurrencies. Skipping...")
                continue

            # Buscar el ID del par en la tabla usdt_pairs
            cursor.execute(
                "SELECT id FROM usdt_pairs WHERE base_currency_id = %s AND quote_currency_id = %s", 
                (base_id[0], quote_id[0])
            )
            pair_id = cursor.fetchone()

            # Si no existe el par en usdt_pairs, saltar este registro
            if pair_id is None:
                print(f"El par {crypto}/{par} no está en usdt_pairs. Skipping...")
                continue

            # Insertar los datos en usdt_data (usando ON CONFLICT DO NOTHING)
            cursor.execute(
                """
                INSERT INTO usdt_data (pair_id, symbol, timestamp, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (pair_id, timestamp) DO NOTHING
                """,
                (pair_id[0], symbol, timestamp, open_price, high_price, low_price, close_price, volume)
            )

        conn.commit()
        print("Datos de USDT insertados con éxito.")

    # Cerrar la conexión
    cursor.close()
    conn.close()

# Llamar la función para insertar los datos en usdt_data
insert_usdt_data_from_csv("processed_cryptos_data_2020_2024.csv")
