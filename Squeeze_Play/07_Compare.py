import pandas as pd
import psycopg2
from decimal import Decimal

def compare_and_generate_csv(csv_path):
    # Database configuration
    conn = psycopg2.connect(dbname='kucoin', user='postgres', password='6962277', host='localhost', port='5432')
    cursor = conn.cursor()

    # Read the CSV file
    csv_data = pd.read_csv(csv_path)

    # Create an empty DataFrame to store the results
    result_df = pd.DataFrame()

    # Iterate through each row in the CSV file
    for index, row in csv_data.iterrows():
        # Extract values from the CSV row
        timestamp = row['timestamp']
        squeeze_up = row['squeeze_up']
        currency = row['currency']
        close_csv = row['close']

        # Fetch the data from historical_data_1day for the current currency and the latest timestamp after the CSV date
        cursor.execute(f"SELECT timestamp, close FROM historical_data_1day WHERE currency = %s AND timestamp >= %s ORDER BY timestamp", (currency, timestamp))
        historical_data = cursor.fetchall()

        if historical_data:
            # Get the latest historical data after the CSV date
            timestamp_table, close_table = historical_data[-1]
            close_table = float(close_table)
            
            # Calculate the percentage difference
            percentage_difference = ((close_table - close_csv) / close_csv) * 100

            # Determine the direction based on the close values
            direction = 'UP' if percentage_difference > 0 else 'DOWN'

            # Find the date and close with the maximum close value after the CSV date
            cursor.execute(f"SELECT timestamp, close FROM historical_data_1day WHERE currency = %s AND timestamp >= %s AND close = (SELECT MAX(close) FROM historical_data_1day WHERE currency = %s AND timestamp >= %s)", (currency, timestamp, currency, timestamp))
            max_close_data = cursor.fetchone()

            if max_close_data:
                max_close_date, max_close_value = max_close_data
                max_close_value = float(max_close_value)
                
                # Calculate the percentage difference with the close from the CSV
                percentage_difference_max = ((max_close_value - close_csv) / close_csv) * 100

                # Create a new DataFrame row
                result_row = {
                    'timestamp_csv': timestamp,
                    'squeeze_up_csv': squeeze_up,
                    'currency': currency,
                    'close_csv': close_csv,
                    'timestamp_table': timestamp_table,
                    'close_table': close_table,
                    'percentage_difference': percentage_difference,
                    'direction': direction,
                    'max_close_date': max_close_date,
                    'max_close_value': max_close_value,
                    'percentage_difference_max': percentage_difference_max
                }

                # Append the row to the result DataFrame
                result_df = pd.concat([result_df, pd.DataFrame([result_row])], ignore_index=True)

    # Export the result DataFrame to a new CSV file
    result_df.to_csv('/home/erosennin/briefcase/Squeeze_Play/comparison_result.csv', index=False)

    # Close the database connection
    cursor.close()
    conn.close()

if __name__ == '__main__':
    compare_and_generate_csv('/home/erosennin/briefcase/Squeeze_Play/listado_2023-11-30 00:00:00_1week.csv')
