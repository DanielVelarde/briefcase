import psycopg2

# Consulta SQL para crear la vista materializada
sql_query = """
CREATE MATERIALIZED VIEW public.usdt_data_ema_daily_view AS
WITH ema_data AS (
    SELECT
        u.id,
        u.pair_id,
        u."timestamp",
        u.open,
        u.high,
        u.low,
        u.close,
        u.volume,
        u.created_at,
        u.symbol,
        -- Calcular la EMA de 10 días sin redondeo
        AVG(u.close) OVER (
            PARTITION BY u.pair_id 
            ORDER BY u.timestamp 
            ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
        ) AS ema_10_day,
        -- Calcular la EMA de 20 días sin redondeo
        AVG(u.close) OVER (
            PARTITION BY u.pair_id 
            ORDER BY u.timestamp 
            ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
        ) AS ema_20_day
    FROM public.usdt_data u
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
    print("Vista materializada 'usdt_data_ema_view' creada exitosamente.")
except Exception as e:
    print(f"Error al crear la vista materializada: {e}")
    conn.rollback()
finally:
    # Cerrar el cursor y la conexión
    cur.close()
    conn.close()
