import pandas as pd
import psycopg2

def get_latest_date(temporalidad):
    # Database configuration
    conn = psycopg2.connect(dbname='kucoin', user='postgres', password='6962277', host='localhost', port='5432')
    cursor = conn.cursor()

    # Fetch the latest date from the squeeze_{temporalidad} table
    cursor.execute(f"SELECT MAX(timestamp) FROM squeeze_{temporalidad}")
    latest_date = cursor.fetchone()[0]

    # Close the database connection
    cursor.close()
    conn.close()

    return latest_date

def generate_filtered_csv(temporalidad):
    # Database configuration
    conn = psycopg2.connect(dbname='kucoin', user='postgres', password='6962277', host='localhost', port='5432')
    cursor = conn.cursor()

    # Obtener la fecha más reciente
    latest_date = get_latest_date(temporalidad)

    # Fetch data from squeeze_{temporalidad} for the latest date where squeeze_up is True
    cursor.execute(f"SELECT timestamp, squeeze_up, currency, close FROM squeeze_{temporalidad} WHERE timestamp::date = %s AND squeeze_up = TRUE", (latest_date,))
    squeeze_data = cursor.fetchall()

    # Create a DataFrame for squeeze_{temporalidad}
    squeeze_df = pd.DataFrame(squeeze_data, columns=["timestamp", "squeeze_up", "currency", "close"])

    # Export the DataFrame to a CSV file
    squeeze_df.to_csv(f'/home/erosennin/briefcase/Squeeze_Play/listado_{latest_date}_{temporalidad}.csv', index=False)

    # Close the database connection
    cursor.close()
    conn.close()

if __name__ == '__main__':
    generate_filtered_csv('1day')  # Generate CSV for daily temporalidad
    generate_filtered_csv('1week')  # Generate CSV for weekly temporalidad
