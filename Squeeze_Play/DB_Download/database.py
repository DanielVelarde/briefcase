import psycopg2
from sqlalchemy import create_engine
import pandas as pd

# Configuración de la base de datos
dbname = "kucoin"
user = "postgres"
password = "6962277"
host = "localhost"
port = "5432"

def establecer_conexion():
    # Establece una conexión con la base de datos PostgreSQL
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cursor = conn.cursor()
        print("Conexión exitosa")
        return conn, cursor
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None, None

def obtener_ultima_fecha_descarga(conn, interval):
    # Obtiene la última fecha de descarga de datos históricos para un intervalo (diario, semanal, mensual)
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT MAX(timestamp) FROM historical_data_{interval}")
        last_date = cursor.fetchone()[0]
        cursor.close()
        return last_date
    except Exception as e:
        print(f"Error al obtener la última fecha de descarga: {e}")
        return None

def guardar_monedas_en_db(conn, cursor, currency_data_list):
    try:
        # Crear la tabla si no existe
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

    except Exception as e:
        print(f"Error al crear la tabla: {e}")

    try:
        # Insertar nuevas monedas sin duplicados
        for currency_data in currency_data_list:
            cursor.execute("""
                INSERT INTO coin_list (currency, name, fullName, precision, isMarginEnabled, isDebitEnabled)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (currency) DO NOTHING
            """, (currency_data['currency'], currency_data['name'], currency_data['fullName'],
                  currency_data['precision'], currency_data['isMarginEnabled'], currency_data['isDebitEnabled']))

        # Confirmar la transacción
        conn.commit()
        print("Datos insertados exitosamente")

    except Exception as e:
        conn.rollback()  # Deshacer cambios en caso de error
        print(f"Error de conexión: {e}")

def guardar_datos_historicos_en_db(conn, cursor, csv_filename, interval):
    # Crea una tabla en la base de datos y guarda datos históricos desde un archivo CSV
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
    historical_data_df.to_sql(f'historical_data_{interval}', engine, if_exists="append", index=False)
