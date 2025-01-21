import psycopg2

def create_fibonacci_view(pair_symbol):
    try:
        # Conexión a la base de datos
        conn = psycopg2.connect(
            dbname="Binance", user="ero", password="6962277", host="localhost", port="5432"
        )
        cursor = conn.cursor()

        # Nombre dinámico de la vista basado en el par elegido
        view_name = f"fibonacci_retracement_{pair_symbol.replace('/', '_')}"
        
        # El SQL para crear la vista dinámica de Fibonacci
        sql = f"""
        DROP VIEW IF EXISTS {view_name};

        CREATE VIEW {view_name} AS
        WITH price_extremes AS (
            SELECT
                symbol,
                MIN(low) AS min_price,
                MAX(high) AS max_price
            FROM
                (
                    SELECT * FROM eth_data
                    UNION ALL
                    SELECT * FROM btc_data
                    UNION ALL
                    SELECT * FROM usdt_data
                ) AS all_data
            WHERE
                symbol = '{pair_symbol}'  -- Aquí se usa el par dinámico
            GROUP BY
                symbol
        ),
        fibonacci_levels AS (
            SELECT
                symbol,
                max_price,
                min_price,
                (max_price - min_price) AS range,
                max_price - ((max_price - min_price) * 0.236) AS fib_23_6,
                max_price - ((max_price - min_price) * 0.382) AS fib_38_2,
                max_price - ((max_price - min_price) * 0.500) AS fib_50_0,
                max_price - ((max_price - min_price) * 0.618) AS fib_61_8,
                max_price - ((max_price - min_price) * 0.786) AS fib_78_6
            FROM price_extremes
        )
        SELECT
            symbol,
            min_price,  -- Mostrar el precio más bajo utilizado
            max_price,  -- Mostrar el precio más alto utilizado
            fib_23_6,
            fib_38_2,
            fib_50_0,
            fib_61_8,
            fib_78_6
        FROM fibonacci_levels;
        """
        
        # Ejecutar el SQL
        cursor.execute(sql)
        conn.commit()
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        print(f"Vista de Fibonacci creada correctamente para el par {pair_symbol}.")
    except Exception as e:
        print(f"Error al crear la vista de Fibonacci: {e}")

# Crear la vista para el par 'ETH/BTC'
create_fibonacci_view('ETH/USDT')
