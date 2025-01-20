import csv
from datetime import datetime

def convert_timestamp_to_datetime(timestamp):
    """
    Convierte un timestamp en milisegundos a un formato de fecha legible para PostgreSQL.
    :param timestamp: Timestamp en milisegundos.
    :return: Fecha en formato 'YYYY-MM-DD HH:MM:SS'.
    """
    # Convertir de milisegundos a segundos
    timestamp_seconds = timestamp / 1000
    # Convertir a datetime y formatear a cadena
    return datetime.utcfromtimestamp(timestamp_seconds).strftime('%Y-%m-%d %H:%M:%S')

def process_csv(input_filename, output_filename):
    """
    Procesa el archivo CSV, convirtiendo los timestamps a formato fecha para PostgreSQL.
    :param input_filename: Nombre del archivo CSV de entrada.
    :param output_filename: Nombre del archivo CSV de salida con fechas formateadas.
    """
    try:
        with open(input_filename, mode="r") as infile, open(output_filename, mode="w", newline="") as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            
            # Leer encabezado y escribirlo en el archivo de salida
            header = next(reader)
            writer.writerow(header)

            # Procesar cada fila y convertir el Timestamp
            for row in reader:
                timestamp = int(row[1])  # El timestamp está en la segunda columna (índice 1)
                row[1] = convert_timestamp_to_datetime(timestamp)
                writer.writerow(row)

        print(f"Archivo procesado con éxito. Los datos se guardaron en {output_filename}")
    
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

if __name__ == "__main__":
    input_filename = "cryptos_with_usdt_btc_eth_historical_data.csv"  # Archivo de entrada
    output_filename = "processed_cryptos_data.csv"  # Archivo de salida con fechas formateadas
    process_csv(input_filename, output_filename)
