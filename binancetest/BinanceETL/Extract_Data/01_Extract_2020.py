import ccxt
import csv
from datetime import datetime, timedelta

# Inicializar la conexión con Binance
exchange = ccxt.binance()

def fetch_historical_data_in_chunks(symbol, timeframe="1d", since=None, limit=500):
    """
    Obtiene datos históricos de Binance en fragmentos para manejar restricciones de la API.
    :param symbol: Par de criptomonedas (e.g., 'BTC/USDT').
    :param timeframe: Intervalo de tiempo ('1d' para diario).
    :param since: Timestamp de inicio en milisegundos.
    :param limit: Máximo número de registros por solicitud (máximo permitido: 500).
    :return: Lista acumulada de datos históricos [timestamp, open, high, low, close, volume].
    """
    all_data = []
    while True:
        try:
            # Obtener datos desde el punto inicial
            data = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
            if not data:
                break

            all_data.extend(data)

            # Actualizar el timestamp de inicio al siguiente intervalo
            since = data[-1][0] + 1  # Siguiente milisegundo después del último timestamp

            # Salir del bucle si no se obtienen 500 registros (fin del rango)
            if len(data) < limit:
                break
        except Exception as e:
            print(f"Error al obtener datos históricos para {symbol}: {e}")
            break

    return all_data

def save_to_single_csv(data, filename):
    """
    Guarda todos los datos históricos en un único archivo CSV consolidado.
    :param data: Lista de datos históricos para múltiples pares de criptomonedas.
    :param filename: Nombre del archivo CSV de salida.
    """
    header = ["Symbol", "Timestamp", "Open", "High", "Low", "Close", "Volume"]

    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)

        print(f"Datos históricos consolidados guardados en {filename}")
    except Exception as e:
        print(f"Error al guardar datos en {filename}: {e}")

if __name__ == "__main__":
    print("Obteniendo datos históricos de las criptomonedas con pares USDT, BTC y ETH en Binance...")

    # Obtener el timestamp de 2020 (1 enero 2020)
    start_date = datetime(2020, 1, 1)
    start_timestamp = int(start_date.timestamp() * 1000)

    # Nombre del archivo consolidado
    consolidated_filename = "cryptos_with_usdt_btc_eth_historical_data_2020_2024.csv"

    # Obtener todos los pares de criptomonedas activos en Binance
    try:
        markets = exchange.fetch_markets()
        # Filtrar solo los pares que incluyen USDT, BTC o ETH
        active_symbols = [
            market["symbol"] for market in markets 
            if market["active"] and ("USDT" in market["symbol"] or "BTC" in market["symbol"] or "ETH" in market["symbol"])
        ]
    except Exception as e:
        print(f"Error al obtener la lista de criptomonedas: {e}")
        active_symbols = []

    if not active_symbols:
        print("No se encontraron pares activos con USDT, BTC o ETH.")
    
    all_historical_data = []

    # Descargar datos en fragmentos de 500 registros
    for symbol in active_symbols:
        print(f"Obteniendo datos históricos para {symbol} desde 2020...")
        historical_data = fetch_historical_data_in_chunks(symbol, "1d", since=start_timestamp)
        
        if historical_data:
            # Agregar el símbolo a cada fila y consolidar
            all_historical_data.extend([[symbol] + row for row in historical_data])
        else:
            print(f"No hay datos históricos disponibles para {symbol}.")

    # Guardar todos los datos en un único archivo CSV
    if all_historical_data:
        save_to_single_csv(all_historical_data, consolidated_filename)
    else:
        print("No se obtuvo ningún dato histórico para guardar.")

    print("Proceso completado.")
