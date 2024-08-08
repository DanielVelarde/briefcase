import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def upload_to_database(temporalidad):
    # Database configuration
    dbname = 'kucoin'
    user = 'postgres'
    password = '6962277'
    host = 'localhost'
    port = '5432'

    # Establish a database connection
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    # Check if the tables exist, and create them if not
    for table_name in ['squeeze_1day', 'squeeze_1week']:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ("
                       "    id SERIAL PRIMARY KEY,"
                       "    timestamp TIMESTAMP,"
                       "    ema10 NUMERIC,"
                       "    ema20 NUMERIC,"
                       "    currency VARCHAR(10),"
                       "    close NUMERIC,"
                       "    squeeze_up BOOLEAN"
                       ");")

    conn.commit()
    # Limpiar las tablas existentes
    for table_name in ['squeeze_1day', 'squeeze_1week']:
        cursor.execute(f"DELETE FROM {table_name};")

    conn.commit()



    # Configuración del motor para usar SQLAlchemy
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')

    # Load the data from the CSV files
    for table_name, temporalidad_csv in zip(['squeeze_1day', 'squeeze_1week'], ['1day', '1week']):
        # Load CSV data
        csv_path = f'/home/erosennin/briefcase/Squeeze_Play/{temporalidad_csv}_latest_data.csv'
        data_df = pd.read_csv(csv_path, parse_dates=['timestamp'])

        # Upload data to the corresponding table
        data_df.to_sql(table_name, engine, if_exists='replace', index=False)

    # Close the database connection
    cursor.close()
    conn.close()

if __name__ == '__main__':
    upload_to_database('1day')
    upload_to_database('1week')
