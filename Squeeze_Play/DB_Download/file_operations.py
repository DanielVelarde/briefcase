# En el archivo file_operations.py
import os
import pandas as pd
from tqdm import tqdm  # Asegúrate de importar tqdm

output_dir = "DB_Download"
# Resto del código en file_operations

# Guarda datos de criptomonedas en un archivo CSV en una ubicación específica
def guardar_monedas_en_csv(currency_data_list, output_dir):
    df = pd.DataFrame(currency_data_list)
    output_filename = "monedas.csv"
    output_path = os.path.join(output_dir, output_filename)

    with tqdm(total=len(df), desc="Guardando datos en CSV") as pbar:
        df.to_csv(output_path, index=False)
        pbar.update(len(df))  # Actualiza el progreso

# Resto del código en file_operations

# Guarda datos históricos en un archivo CSV en una ubicación específica
def guardar_datos_historicos_en_csv(historical_data, interval):
    columns = ["timestamp", "open", "high", "low", "close", "volume", "assetvolume", "currency"]
    output_filename = f"historical_data_{interval}.csv"
    output_path = os.path.join(output_dir, output_filename)

    historical_df = pd.DataFrame(historical_data, columns=columns)

    with tqdm(total=len(historical_df), desc=f"Guardando datos históricos ({interval}) en CSV") as pbar:
        historical_df.to_csv(output_path, index=False)
        pbar.update(len(historical_df))  # Actualiza el progreso

    return output_path
