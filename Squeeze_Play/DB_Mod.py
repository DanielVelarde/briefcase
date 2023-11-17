import psycopg2

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
        # Crear tabla coin_list
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

        # Crear tablas historical_data_1day y historical_data_1week
        intervals = ["1day", "1week"]
        for interval in intervals:
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS historical_data_{interval} (
                timestamp TIMESTAMP,
                open NUMERIC,
                high NUMERIC,
                low NUMERIC,
                close NUMERIC,
                volume NUMERIC,
                assetvolume NUMERIC,
                currency VARCHAR REFERENCES coin_list (currency)
            );
            """
            cursor.execute(create_table_query)
            conn.commit()
            print(f"Tabla 'historical_data_{interval}' creada o ya existe")

        cursor.close()
        conn.close()

def crear_indices():
    conn, cursor = establecer_conexion()
    if conn is not None and cursor is not None:
        # Crear índice en la columna timestamp de historical_data_1day
        cursor.execute("CREATE INDEX idx_timestamp_1day ON historical_data_1day (timestamp);")
        conn.commit()
        print("Índice en 'timestamp' de 'historical_data_1day' creado")

        # Crear índice en la columna timestamp de historical_data_1week
        cursor.execute("CREATE INDEX idx_timestamp_1week ON historical_data_1week (timestamp);")
        conn.commit()
        print("Índice en 'timestamp' de 'historical_data_1week' creado")

        # Crear índice en la columna currency de coin_list
        cursor.execute("CREATE INDEX idx_currency_coin_list ON coin_list (currency);")
        conn.commit()
        print("Índice en 'currency' de 'coin_list' creado")

        cursor.close()
        conn.close()

def establecer_relaciones():
    conn, cursor = establecer_conexion()
    if conn is not None and cursor is not None:
        # Establecer relaciones en historical_data_1day
        cursor.execute("""
            ALTER TABLE historical_data_1day
            ADD FOREIGN KEY (currency) REFERENCES coin_list (currency);
        """)
        conn.commit()
        print("Relación en 'historical_data_1day' establecida con 'coin_list'")

        # Establecer relaciones en historical_data_1week
        cursor.execute("""
            ALTER TABLE historical_data_1week
            ADD FOREIGN KEY (currency) REFERENCES coin_list (currency);
        """)
        conn.commit()
        print("Relación en 'historical_data_1week' establecida con 'coin_list'")

        cursor.close()
        conn.close()

if __name__ == "__main__":
    crear_tablas_si_no_existen()
    crear_indices()
    establecer_relaciones()
