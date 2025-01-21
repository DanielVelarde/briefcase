import psycopg2
import pandas as pd
import plotly.graph_objects as go

# Conectar a la base de datos
conn = psycopg2.connect(
    dbname="Binance",
    user="ero",
    password="6962277",
    host="localhost",
    port="5432"
)

# Consultar todos los pares disponibles para ETH
query_pairs = """
SELECT
    ep.id,
    ep.symbol
FROM public.eth_pairs ep;
"""

# Cargar los datos en un DataFrame
eth_pairs_df = pd.read_sql(query_pairs, conn)

# Ver los pares disponibles
print(eth_pairs_df)

# Asegurémonos de que el pair_id de ETH sea correcto. Supongamos que es 1
pair_id_eth = 1  # Cambiar este valor si es necesario

# Consultar los datos de la vista materializada para ETH con el pair_id correcto
query_eth_daily = f"""
SELECT
    eth."timestamp",  -- Fecha
    eth.open,
    eth.high,
    eth.low,
    eth.close,
    eth.ema_10_day,  -- EMA de 10 días
    eth.ema_20_day,  -- EMA de 20 días
    ep.symbol
FROM public.eth_data_ema_daily_view eth
JOIN public.eth_pairs ep ON eth.pair_id = ep.id
WHERE eth.pair_id = {pair_id_eth}  -- Filtrar solo por el par con el pair_id correcto
ORDER BY eth."timestamp";
"""

# Cargar los datos en un DataFrame
eth_daily_df = pd.read_sql(query_eth_daily, conn)

# Cerrar la conexión a la base de datos
conn.close()

# Verificar si se están obteniendo datos
print(eth_daily_df.head())

# Si se tienen datos, continuar con la creación del gráfico
if not eth_daily_df.empty:
    # Obtener el nombre del par
    pair_name = eth_daily_df['symbol'].iloc[0]

    # Graficar las velas japonesas y las EMAs utilizando Plotly
    fig = go.Figure(data=[

        # Velas japonesas
        go.Candlestick(
            x=eth_daily_df['timestamp'],
            open=eth_daily_df['open'],
            high=eth_daily_df['high'],
            low=eth_daily_df['low'],
            close=eth_daily_df['close'],
            name='Candlestick'
        ),

        # EMA 10
        go.Scatter(
            x=eth_daily_df['timestamp'],
            y=eth_daily_df['ema_10_day'],
            mode='lines',
            name='EMA 10',
            line=dict(color='blue')
        ),

        # EMA 20
        go.Scatter(
            x=eth_daily_df['timestamp'],
            y=eth_daily_df['ema_20_day'],
            mode='lines',
            name='EMA 20',
            line=dict(color='red')
        )

    ])

    # Actualizar el diseño del gráfico
    fig.update_layout(
        title=f'Gráfico de Velas Japonesas con EMAs 10 y 20 - {pair_name}',  # Mostrar el nombre del par en el título
        xaxis_title='Fecha',
        yaxis_title='Precio',
        xaxis_rangeslider_visible=False,  # Desactivar el control de rango
        template='plotly_dark',  # Estilo oscuro para el gráfico
    )

    # Mostrar el gráfico
    fig.show()
else:
    print("No se encontraron datos para el par ETH.")
