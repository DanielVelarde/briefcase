README
Overview

This Python script is designed to fetch historical price data for various cryptocurrencies from the KuCoin exchange. The data is retrieved using the KuCoin API and stored in a PostgreSQL database. The script supports different time intervals, such as daily (1day) and weekly (1week).
Prerequisites

Make sure you have the following dependencies installed:

    Python 3.x
    PostgreSQL
    Required Python packages (install using pip install package_name):
        psycopg2
        requests
        pandas
        sqlalchemy
        tqdm

Setup

    Clone the repository:

    bash

git clone https://github.com/your-username/kucoin-historical-data.git

Create a virtual environment (optional but recommended):

bash

cd kucoin-historical-data
python -m venv venv

Activate the virtual environment:

    Windows:

    bash

.\venv\Scripts\activate

Unix or MacOS:

bash

    source venv/bin/activate

Install the required packages:

bash

    pip install -r requirements.txt

    Configure your PostgreSQL database connection in the script:
        Open kucoin_data_downloader.py in a text editor.
        Update the dbname, user, password, host, and port variables according to your PostgreSQL setup.

Usage

Run the script to fetch and store historical data:

bash

python kucoin_data_downloader.py

Understanding the Code

    Database Setup:
        The script creates tables for different time intervals in the PostgreSQL database if they do not exist.
        Coin information is stored in the coin_list table.

    Data Retrieval:
        The script fetches a list of supported cryptocurrencies from the KuCoin API.
        It then downloads historical price data for each cryptocurrency and stores it in the corresponding database table.

    Data Storage:
        Timestamps are stored in UTC format.
        Data is stored in CSV files and loaded into the database using Pandas and SQLAlchemy.

Additional Notes

    Adjust the time intervals or add new ones as needed by modifying the intervals list in the script.
    The script avoids downloading duplicate data by checking the last stored timestamp in the database.

README (en español)
Descripción general

Este script de Python está diseñado para obtener datos históricos de precios de diversas criptomonedas del exchange KuCoin. Los datos se recuperan utilizando la API de KuCoin y se almacenan en una base de datos PostgreSQL. El script es compatible con diferentes intervalos de tiempo, como diario (1day) y semanal (1week).
Requisitos previos

Asegúrate de tener instaladas las siguientes dependencias:

    Python 3.x
    PostgreSQL
    Paquetes de Python necesarios (instálalos con pip install nombre_del_paquete):
        psycopg2
        requests
        pandas
        sqlalchemy
        tqdm

Configuración

    Clona el repositorio:

    bash

git clone https://github.com/tu-nombre-de-usuario/kucoin-historical-data.git

Crea un entorno virtual (opcional pero recomendado):

bash

cd kucoin-historical-data
python -m venv venv

Activa el entorno virtual:

    Windows:

    bash

.\venv\Scripts\activate

Unix o MacOS:

bash

    source venv/bin/activate

Instala los paquetes necesarios:

bash

    pip install -r requirements.txt

    Configura la conexión a tu base de datos PostgreSQL en el script:
        Abre kucoin_data_downloader.py en un editor de texto.
        Actualiza las variables dbname, user, password, host y port según tu configuración de PostgreSQL.

Uso

Ejecuta el script para obtener y almacenar datos históricos:

bash

python kucoin_data_downloader.py

Entendiendo el código

    Configuración de la base de datos:
        El script crea tablas para diferentes intervalos de tiempo en la base de datos PostgreSQL si no existen.
        La información de las criptomonedas se almacena en la tabla coin_list.

    Recuperación de datos:
        El script obtiene una lista de criptomonedas admitidas de la API de KuCoin.
        Luego descarga datos históricos de precios para cada criptomoneda y los almacena en la tabla correspondiente de la base de datos.

    Almacenamiento de datos:
        Los registros de tiempo se almacenan en formato UTC.
        Los datos se almacenan en archivos CSV y se cargan en la base de datos utilizando Pandas y SQLAlchemy.

Notas adicionales

    Ajusta los intervalos de tiempo o agrega nuevos según sea necesario modificando la lista intervals en el script.
    El script evita descargar datos duplicados mediante la verificación del último timestamp almacenado en la base de datos.