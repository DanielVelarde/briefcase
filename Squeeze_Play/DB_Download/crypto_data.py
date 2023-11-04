import requests
from tqdm import tqdm

def obtener_lista_monedas():
    # Obtiene la lista de criptomonedas desde una API de KuCoin
    api_url = 'https://api.kucoin.com/api/v3/currencies'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        currencies = data.get('data', [])
        return currencies
    else:
        print("Error al obtener la lista de monedas")
        return []

def obtener_datos_historicos(interval, coins):
    # Obtiene datos históricos de precios de criptomonedas para un intervalo (diario, semanal, mensual)
    historical_data = []

    for currency in coins:
        symbol = f"{currency['currency']}-USDT"
        url = f"https://api.kucoin.com/api/v1/market/candles?type={interval}&symbol={symbol}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data["code"] == "200000":
                    historical_prices = data["data"]
                    if historical_prices:
                        total = len(historical_prices)
                        with tqdm(total=total, position=0, leave=True, ncols=100, desc=f"Obteniendo datos para {currency['currency']}") as pbar:
                            for price_data in historical_prices:
                                price_data.append(currency['currency'])
                                historical_data.append(price_data)
                                pbar.update(1)  # Actualizar la barra de progreso
                    else:
                        continue
                else:
                    continue
            else:
                print(f"Error al obtener datos históricos para {currency}: Código de estado {response.status_code}")
        except Exception as e:
            print(f"Error de conexión para {currency}: {e}")

    return historical_data
