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

# Consulta SQL para las velas semanales
candlestick_query = """
WITH weekly_data AS (
    SELECT 
        date_trunc('week', "timestamp") AS week_start,
        MIN(low) AS low,
        MAX(high) AS high,
        (ARRAY_AGG(open ORDER BY "timestamp"))[1] AS open,
        (ARRAY_AGG(close ORDER BY "timestamp"))[array_length(ARRAY_AGG(close ORDER BY "timestamp"), 1)] AS close
    FROM eth_data
    WHERE symbol = 'ETH/BTC'
    GROUP BY date_trunc('week', "timestamp")
)
SELECT *
FROM weekly_data
ORDER BY week_start;
"""

# Consulta SQL para obtener los niveles de soporte y resistencia
support_resistance_query = """
SELECT * FROM eth_btc_supports_resistances;
"""

# Cargar los datos de velas y niveles de soporte/resistencia
candlestick_df = pd.read_sql(candlestick_query, conn)
levels_df = pd.read_sql(support_resistance_query, conn)

# Cerrar la conexión
conn.close()

# Graficar las velas japonesas y los niveles de soporte y resistencia usando Plotly
fig = go.Figure(data=[

    # Velas japonesas
    go.Candlestick(
        x=candlestick_df['week_start'],
        open=candlestick_df['open'],
        high=candlestick_df['high'],
        low=candlestick_df['low'],
        close=candlestick_df['close'],
        name='Candlestick'
    ),
])

# Agregar líneas de soporte y resistencia
for level in levels_df['level']:
    fig.add_trace(go.Scatter(
        x=candlestick_df['week_start'],
        y=[level] * len(candlestick_df),  # Duplicar el nivel para todo el gráfico
        mode='lines',
        name=f'Support/Resistance at {level}',
        line=dict(color='red', dash='dash')
    ))

# Actualizar el diseño del gráfico
fig.update_layout(
    title='ETH/BTC Weekly Candlestick Chart with Support and Resistance Levels',
    xaxis_title='Fecha',
    yaxis_title='Precio (BTC)',
    xaxis_rangeslider_visible=False,  # Desactivar el control de rango
    template='plotly_dark',  # Estilo oscuro para el gráfico
)

# Mostrar el gráfico en el navegador
fig.show()
