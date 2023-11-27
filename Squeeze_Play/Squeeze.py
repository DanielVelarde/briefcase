import pandas as pd
import psycopg2

def generate_csv(temporalidad):
    # Database configuration
    conn = psycopg2.connect(dbname='kucoin', user='postgres', password='6962277', host='localhost', port='5432')
    cursor = conn.cursor()

    # Fetch all currencies from the coin_list table
    cursor.execute("SELECT DISTINCT currency FROM coin_list")
    currencies = cursor.fetchall()

    # Create an empty DataFrame to store the results
    result_df = pd.DataFrame()

    # Iterate through each currency
    for currency in currencies:
        coin = currency[0]

        # Fetch data for the current currency from ema_{temporalidad}
        cursor.execute(f"SELECT timestamp, ema10, ema20, currency FROM ema_{temporalidad} WHERE currency = %s ORDER BY timestamp DESC LIMIT 5", (coin,))
        ema_data = cursor.fetchall()

        # Create a DataFrame for ema_{temporalidad}
        ema_df = pd.DataFrame(ema_data, columns=["timestamp", "ema10", "ema20", "currency"])

        # Fetch data for the current currency from historical_data_{temporalidad}
        cursor.execute(f"SELECT timestamp, close FROM historical_data_{temporalidad} WHERE currency = %s ORDER BY timestamp DESC LIMIT 5", (coin,))
        historical_data = cursor.fetchall()

        # Create a DataFrame for historical_data_{temporalidad}
        historical_df = pd.DataFrame(historical_data, columns=["timestamp", "close"])

        # Merge the two DataFrames on the 'timestamp' column
        merged_df = pd.merge(ema_df, historical_df, on="timestamp")

        # Add the merged data to the main DataFrame
        result_df = pd.concat([result_df, merged_df], ignore_index=True)

    # Add a boolean column 'squeeze_up' based on the specified conditions
    result_df['squeeze_up'] = (result_df['close'] < result_df['ema20']) & (result_df['close'] > result_df['ema10'])

    # Export the main DataFrame to a CSV file with the original timestamp format
    result_df.to_csv(f'/home/erosennin/briefcase/Squeeze_Play/{temporalidad}_latest_data.csv', index=False, date_format="%Y-%m-%d %H:%M:%S")

    # Close the database connection
    cursor.close()
    conn.close()

if __name__ == '__main__':
    generate_csv('1day')  # Generate CSV for daily temporalidad
    generate_csv('1week')  # Generate CSV for weekly temporalidad
