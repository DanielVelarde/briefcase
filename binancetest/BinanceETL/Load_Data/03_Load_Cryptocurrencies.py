import psycopg2
import csv

# Conexión a la base de datos
def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname="Binance", 
            user="ero", 
            password="6962277", 
            host="localhost", 
            port="5432"
        )
        return connection
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Insertar los datos de cada fila en la tabla 'cryptocurrencies'
def insert_data(cursor, symbol, name):
    try:
        # Insertar los datos en la tabla 'cryptocurrencies'
        insert_query = """
        INSERT INTO cryptocurrencies (symbol, name)
        VALUES (%s, %s)
        ON CONFLICT (symbol) DO NOTHING;  -- No insertar si ya existe el símbolo
        """
        cursor.execute(insert_query, (symbol, name))
    except Exception as e:
        print(f"Error al insertar el dato {symbol}: {e}")
        cursor.connection.rollback()  # Revertir cualquier cambio hecho durante la transacción fallida

# Procesar el archivo CSV e insertar los datos en la base de datos
def process_csv_and_insert(input_filename):
    connection = connect_to_db()
    if connection is None:
        return

    cursor = connection.cursor()

    try:
        with open(input_filename, mode="r") as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                symbol = row['Symbol']
                crypto = row['Crypto']

                # Iniciar una nueva transacción para cada inserción
                connection.autocommit = False  # Desactivar autocommit para manejo manual de transacciones
                insert_data(cursor, symbol, crypto)
                connection.commit()  # Confirmar la transacción actual

            print("Datos insertados correctamente en la tabla 'cryptocurrencies'.")

    except Exception as e:
        print(f"Error al procesar el archivo CSV: {e}")
        connection.rollback()  # Revertir los cambios si ocurre un error
    finally:
        # Cerrar la conexión
        cursor.close()
        connection.close()

if __name__ == "__main__":
    input_filename = "processed_cryptos_data.csv"  # Archivo CSV con las columnas 'Crypto' y 'Par'
    process_csv_and_insert(input_filename)
