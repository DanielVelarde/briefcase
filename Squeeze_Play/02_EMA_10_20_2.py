import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Database configuration
dbname = "kucoin"
user = "postgres"
password = "6962277"
host = "localhost"
port = "5432"

# Establish a database connection
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cursor = conn.cursor()
# Create new tables ema_diaria and ema_semanal if they don't exist
for temporalidad in ['1day', '1week']:
    try:
        cursor.execute(f'CREATE TABLE IF NOT EXISTS ema_{temporalidad} ('
                       '    id SERIAL PRIMARY KEY,'
                       '    timestamp TIMESTAMP,'
                       '    close NUMERIC,'
                       '    ema10 NUMERIC,'
                       '    ema20 NUMERIC,'
                       '    currency VARCHAR(10) REFERENCES coin_list(currency)'
                       ');')
        # Create index on the currency column
        cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_currency_{temporalidad} ON ema_{temporalidad} (currency);')
    except Exception as e:
        print(f'Error al crear la tabla ema_{temporalidad}: {e}')

# Limpiar las tablas ema_day y ema_week
cursor.execute("DELETE FROM ema_1day")
cursor.execute("DELETE FROM ema_1week")
conn.commit()

# Fetch all currencies from the coin_list table
cursor.execute("SELECT DISTINCT currency FROM coin_list")
currencies = cursor.fetchall()

# Create empty DataFrames to store the results
daily_result_df = pd.DataFrame()
weekly_result_df = pd.DataFrame()

# Function to calculate EMA
def calculate_ema(data, period):
    ema = data['close'].ewm(span=period, adjust=False).mean()
    return ema



conn.commit()
# Iterate through each currency
for currency in currencies:
    # Extract the currency symbol from the tuple
    coin = currency[0]

    # Fetch daily and weekly data for the current currency
    cursor.execute(f"SELECT timestamp, close FROM historical_data_1day WHERE currency = %s ORDER BY timestamp", (coin,))
    daily_data = cursor.fetchall()

    cursor.execute(f"SELECT timestamp, close FROM historical_data_1week WHERE currency = %s ORDER BY timestamp", (coin,))
    weekly_data = cursor.fetchall()

    # Create DataFrames
    daily_df = pd.DataFrame(daily_data, columns=["timestamp", "close"])
    weekly_df = pd.DataFrame(weekly_data, columns=["timestamp", "close"])

    # Calculate EMA 10 and 20
    daily_df['ema10'] = calculate_ema(daily_df, 10)
    daily_df['ema20'] = calculate_ema(daily_df, 20)

    weekly_df['ema10'] = calculate_ema(weekly_df, 10)
    weekly_df['ema20'] = calculate_ema(weekly_df, 20)

    # Add 'currency' column to DataFrames
    daily_df['currency'] = coin
    weekly_df['currency'] = coin

    # Concatenate the results to the main DataFrames
    daily_result_df = pd.concat([daily_result_df, daily_df[['timestamp', 'ema10', 'ema20', 'currency']]], ignore_index=True)
    weekly_result_df = pd.concat([weekly_result_df, weekly_df[['timestamp', 'ema10', 'ema20', 'currency']]], ignore_index=True)

# Export the main DataFrames to CSV files with the original timestamp format
daily_result_df.to_csv('/home/erosennin/briefcase/Squeeze_Play/daily_emas_results.csv', index=False, date_format='%Y-%m-%d %H:%M:%S')
weekly_result_df.to_csv('/home/erosennin/briefcase/Squeeze_Play/weekly_emas_results.csv', index=False, date_format='%Y-%m-%d %H:%M:%S')

# Close the database connection
cursor.close()
conn.close()

# Database configuration for SQLAlchemy
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')

# Load data from CSV to database tables
try:
    daily_result_df = pd.read_csv('/home/erosennin/briefcase/Squeeze_Play/daily_emas_results.csv', parse_dates=['timestamp'], infer_datetime_format=True)
    daily_result_df.to_sql('ema_1day', engine, if_exists='replace', index=False)

    weekly_result_df = pd.read_csv('/home/erosennin/briefcase/Squeeze_Play/weekly_emas_results.csv', parse_dates=['timestamp'], infer_datetime_format=True)
    weekly_result_df.to_sql('ema_1week', engine, if_exists='replace', index=False)
except Exception as e:
    print(f'Error al cargar datos en las tablas: {e}')
