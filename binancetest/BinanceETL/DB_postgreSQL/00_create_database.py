import psycopg2
from psycopg2 import sql

def execute_sql_file(database_name, user, password, host, port, sql_file_path):
    try:
        # Conectar a PostgreSQL como superusuario o usuario con permisos para crear bases de datos
        conn = psycopg2.connect(
            dbname="postgres",  # Usamos la base de datos por defecto para conectarnos
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True  # Necesario para operaciones fuera de transacciones (como crear DB)
        cursor = conn.cursor()

        # Intentar crear la base de datos si no existe
        print(f"Creando la base de datos '{database_name}'...")
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name))
        )
        print(f"Base de datos '{database_name}' creada con éxito.")

        # Cerrar conexión al servidor principal
        cursor.close()
        conn.close()

        # Conectar a la nueva base de datos
        conn = psycopg2.connect(
            dbname=database_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()

        # Leer y ejecutar el archivo SQL
        print(f"Ejecutando el archivo SQL '{sql_file_path}' en la base de datos '{database_name}'...")
        with open(sql_file_path, "r") as file:
            sql_commands = file.read()
            cursor.execute(sql_commands)

        conn.commit()
        print("Estructura de la base de datos creada con éxito.")

        # Cerrar conexión
        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Error al ejecutar el archivo SQL: {e}")
    except FileNotFoundError:
        print(f"Archivo '{sql_file_path}' no encontrado.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Parámetros de configuración
DATABASE_NAME = "Binance"          # Nombre de la base de datos a crear
USER = "ero"                      # Usuario de PostgreSQL
PASSWORD = "6962277"              # Contraseña del usuario
HOST = "localhost"                # Host del servidor PostgreSQL
PORT = 5432                       # Puerto del servidor PostgreSQL
SQL_FILE_PATH = "/home/erosennin/briefcase/binancetest/estructura_base.sql"  # Ruta al archivo SQL

# Ejecutar el script
execute_sql_file(DATABASE_NAME, USER, PASSWORD, HOST, PORT, SQL_FILE_PATH)
