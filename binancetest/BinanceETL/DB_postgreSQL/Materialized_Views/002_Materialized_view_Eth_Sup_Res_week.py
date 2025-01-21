import psycopg2

# Datos de conexión a la base de datos
dbname = "Binance"
user = "ero"
password = "6962277"
host = "localhost"
port = "5432"

# Conectar a la base de datos
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Crear un cursor para ejecutar la consulta
cur = conn.cursor()

# El código SQL para crear la vista materializada
sql_create_view = """
-- Crear la vista materializada para soportes y resistencias semanales del par ETH/BTC
DROP MATERIALIZED VIEW IF EXISTS eth_btc_supports_resistances;

CREATE MATERIALIZED VIEW eth_btc_supports_resistances AS
WITH weekly_data AS (
    SELECT
        date_trunc('week', "timestamp") AS week_start,
        MIN(low) AS weekly_low,
        MAX(high) AS weekly_high
    FROM eth_data
    WHERE symbol = 'ETH/BTC'
    GROUP BY date_trunc('week', "timestamp")
),
extremes AS (
    SELECT
        weekly_low AS level,
        'support' AS type
    FROM weekly_data
    UNION ALL
    SELECT
        weekly_high AS level,
        'resistance' AS type
    FROM weekly_data
),
touch_count AS (
    SELECT
        level,
        COUNT(*) AS touches,
        type
    FROM extremes
    GROUP BY level, type
),
ranked_levels AS (
    SELECT
        level,
        touches,
        type,
        ROW_NUMBER() OVER (PARTITION BY type ORDER BY touches DESC) AS rank
    FROM touch_count
)
SELECT
    level,
    type
FROM ranked_levels
WHERE rank <= 10
ORDER BY type, level;

-- Crear un índice para mejorar el rendimiento al consultar la vista materializada
CREATE INDEX idx_eth_btc_supports_resistances ON eth_btc_supports_resistances (type, level);
"""

# Ejecutar la consulta SQL
try:
    cur.execute(sql_create_view)
    conn.commit()  # Confirmar los cambios
    print("Vista materializada 'eth_btc_supports_resistances' creada/actualizada exitosamente.")
except Exception as e:
    print(f"Ocurrió un error al ejecutar el SQL: {e}")
    conn.rollback()  # Si ocurre un error, deshacer los cambios

# Cerrar el cursor y la conexión
cur.close()
conn.close()
