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

# Consultar los datos de la vista materializada para BTC con pair_id = 1
query_btc = """
SELECT
    btc."week_start",
    btc.avg_open,
    btc.avg_high,
    btc.avg_low,
    btc.avg_close,
    btc.ema_10_week,
    btc.ema_20_week,
    bp.symbol
FROM public.btc_data_ema_weekly_view btc
JOIN public.btc_pairs bp ON btc.pair_id = bp.id
WHERE btc.pair_id = 1  -- Filtrar solo por el par con id = 1
ORDER BY btc."week_start";
"""

# Cargar los datos en un DataFrame
btc_df = pd.read_sql(query_btc, conn)

# Cerrar la conexión a la base de datos
conn.close()

# Obtener el nombre del par
pair_name = btc_df['symbol'].iloc[0]

# Graficar las velas japonesas y las EMAs utilizando Plotly
fig = go.Figure(data=[

    # Velas japonesas
    go.Candlestick(
        x=btc_df['week_start'],
        open=btc_df['avg_open'],
        high=btc_df['avg_high'],
        low=btc_df['avg_low'],
        close=btc_df['avg_close'],
        name='Candlestick'
    ),

    # EMA 10
    go.Scatter(
        x=btc_df['week_start'],
        y=btc_df['ema_10_week'],
        mode='lines',
        name='EMA 10',
        line=dict(color='blue')
    ),

    # EMA 20
    go.Scatter(
        x=btc_df['week_start'],
        y=btc_df['ema_20_week'],
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
