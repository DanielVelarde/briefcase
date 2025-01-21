import psycopg2

# Consulta SQL para crear la vista materializada
sql_query = """
CREATE MATERIALIZED VIEW public.btc_data_ema_daily_view AS
WITH ema_data AS (
    SELECT
        b.id,
        b.pair_id,
        b."timestamp",
        b.open,
        b.high,
        b.low,
        b.close,
        b.volume,
        b.created_at,
        b.symbol,
        -- Calcular la EMA de 10 días sin redondeo
        AVG(b.close) OVER (
            PARTITION BY b.pair_id 
            ORDER BY b.timestamp 
            ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
        ) AS ema_10_day,
        -- Calcular la EMA de 20 días sin redondeo
        AVG(b.close) OVER (
            PARTITION BY b.pair_id 
            ORDER BY b.timestamp 
            ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
        ) AS ema_20_day
    FROM public.btc_data b
)
SELECT * FROM ema_data;
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
    cur.execute(sql_query)

    # Confirmar los cambios
    conn.commit()
    print("Vista materializada creada exitosamente.")
except Exception as e:
    print(f"Error al crear la vista materializada: {e}")
    conn.rollback()
finally:
    # Cerrar el cursor y la conexión
    cur.close()
    conn.close()
