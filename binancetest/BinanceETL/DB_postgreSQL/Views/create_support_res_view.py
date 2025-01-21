import psycopg2

# Datos de conexión a la base de datos
dbname = "Binance"
user = "ero"
password = "6962277"
host = "localhost"
port = "5432"

# Función para crear la vista de soportes y resistencias para un par específico
def create_support_res_view(symbol):
    # Conectar a la base de datos
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cur = conn.cursor()

    # Determinar el nombre de la tabla de datos y la tabla de pares según el símbolo
    if 'ETH' in symbol:
        data_table = 'eth_data'
        pairs_table = 'eth_pairs'
    elif 'BTC' in symbol:
        data_table = 'btc_data'
        pairs_table = 'btc_pairs'
    elif 'USDT' in symbol:
        data_table = 'usdt_data'
        pairs_table = 'usdt_pairs'
    else:
        print(f"Símbolo {symbol} no reconocido. Asegúrate de usar ETH, BTC o USDT.")
        return

    # Escapar el símbolo del par para el nombre de la vista
    view_name = symbol.replace('/', '_')

    # Consulta SQL para crear la vista del par específico
    sql_create_view = f"""
    DROP VIEW IF EXISTS "{view_name}_supports_resistances";

    CREATE VIEW "{view_name}_supports_resistances" AS
    WITH weekly_data AS (
        SELECT
            date_trunc('week', "timestamp") AS week_start,
            MIN(low) AS weekly_low,
            MAX(high) AS weekly_high
        FROM {data_table}
        JOIN {pairs_table} AS p ON {data_table}.pair_id = p.id
        WHERE p.symbol = '{symbol}'
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
    """

    try:
        # Ejecutar la consulta para crear la vista
        cur.execute(sql_create_view)
        conn.commit()  # Confirmar los cambios
        print(f"Vista '{view_name}_supports_resistances' creada exitosamente.")
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el SQL: {e}")
        conn.rollback()  # Si ocurre un error, deshacer los cambios
    finally:
        # Cerrar el cursor y la conexión
        cur.close()
        conn.close()

# Llamada a la función con el símbolo deseado
# Por ejemplo, para ETH/BTC:
create_support_res_view('SEI/USDT')
# También puedes probar con otros pares como 'ETH/USDT', 'BNB/ETH', etc.
