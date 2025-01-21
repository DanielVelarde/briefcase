import psycopg2

# Consulta SQL para crear la vista materializada con EMAs en temporalidad semanal
sql_query_weekly = """
CREATE MATERIALIZED VIEW public.btc_data_ema_weekly_view AS
WITH weekly_data AS (
    SELECT
        b.pair_id,
        date_trunc('week', b."timestamp") AS week_start,
        AVG(b.open) AS avg_open,
        AVG(b.high) AS avg_high,
        AVG(b.low) AS avg_low,
        AVG(b.close) AS avg_close,
        AVG(b.volume) AS avg_volume
    FROM public.btc_data b
    GROUP BY b.pair_id, date_trunc('week', b."timestamp")
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
    # Ejecutar la consulta para crear la vista materializada
    cur.execute(sql_query_weekly)

    # Confirmar los cambios
    conn.commit()
    print("Vista materializada 'btc_data_ema_weekly_view' creada exitosamente.")
except Exception as e:
    print(f"Error al crear la vista materializada: {e}")
    conn.rollback()
finally:
    # Cerrar el cursor y la conexión
    cur.close()
    conn.close()
