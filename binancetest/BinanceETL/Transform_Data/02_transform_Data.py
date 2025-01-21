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
    Procesa el archivo CSV, separando la columna 'Symbol' en 'Crypto' y 'Par', 
    y convirtiendo los timestamps a formato fecha para PostgreSQL.
    :param input_filename: Nombre del archivo CSV de entrada.
    :param output_filename: Nombre del archivo CSV de salida con fechas formateadas y columnas separadas.
    """
    try:
        with open(input_filename, mode="r") as infile, open(output_filename, mode="w", newline="") as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            
            # Leer encabezado y escribirlo en el archivo de salida
            header = next(reader)
            # Agregar las nuevas columnas en el encabezado
            header.append('Crypto')
            header.append('Par')
            writer.writerow(header)

            # Procesar cada fila
            for row in reader:
                symbol = row[0]  # La columna 'Symbol' está en la primera posición (índice 0)
                timestamp = int(row[1])  # El timestamp está en la segunda columna (índice 1)
                
                # Separar el símbolo en 'Crypto' y 'Par'
                crypto, par = symbol.split('/')  # Separar por '/'
                row[0] = symbol  # Mantener la columna 'Symbol' original
                row.append(crypto)  # Añadir la columna 'Crypto'
                row.append(par)  # Añadir la columna 'Par'
                
                # Convertir el timestamp a formato de fecha
                row[1] = convert_timestamp_to_datetime(timestamp)
                
                # Escribir la fila procesada en el archivo de salida
                writer.writerow(row)

        print(f"Archivo procesado con éxito. Los datos se guardaron en {output_filename}")
    
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

if __name__ == "__main__":
    input_filename = "cryptos_with_usdt_btc_eth_historical_data_2020_2024.csv"  # Archivo de entrada
    output_filename = "processed_cryptos_data_2020_2024.csv"  # Archivo de salida con fechas formateadas y columnas separadas
    process_csv(input_filename, output_filename)
