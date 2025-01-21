import psycopg2

# Consulta SQL para crear la vista materializada con EMAs en temporalidad semanal para ETH
sql_query_weekly_eth = """
CREATE MATERIALIZED VIEW public.eth_data_ema_weekly_view AS
WITH weekly_data AS (
    SELECT
        e.pair_id,
        date_trunc('week', e."timestamp") AS week_start,
        AVG(e.open) AS avg_open,
        AVG(e.high) AS avg_high,
        AVG(e.low) AS avg_low,
        AVG(e.close) AS avg_close,
        AVG(e.volume) AS avg_volume
    FROM public.eth_data e
    GROUP BY e.pair_id, date_trunc('week', e."timestamp")
),
ema_data_weekly AS (
    SELECT
        w.pair_id,
        w.week_start,
        w.avg_open,
        w.avg_high,
        w.avg_low,
        w.avg_close,
        w.avg_volume,
        -- Calcular la EMA de 10 semanas sin redondeo
        AVG(w.avg_close) OVER (
            PARTITION BY w.pair_id
            ORDER BY w.week_start
            ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
        ) AS ema_10_week,
        -- Calcular la EMA de 20 semanas sin redondeo
        AVG(w.avg_close) OVER (
            PARTITION BY w.pair_id
            ORDER BY w.week_start
            ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
        ) AS ema_20_week
    FROM weekly_data w
)
SELECT * FROM ema_data_weekly;
"""

# Establecer la conexión a la base de datos
conn = psycopg2.connect(
    dbname="Binance",
    user="ero",
    password="6962277",
    host="localhost",
    port="5432"
)

# Crear un cursor para ejecutar las consultas
cur = conn.cursor()

try:
    # Ejecutar la consulta para crear la vista materializada para ETH
    cur.execute(sql_query_weekly_eth)

    # Confirmar los cambios
    conn.commit()
    print("Vista materializada 'eth_data_ema_weekly_view' creada exitosamente.")
except Exception as e:
    print(f"Error al crear la vista materializada: {e}")
    conn.rollback()
finally:
    # Cerrar el cursor y la conexión
    cur.close()
    conn.close()
