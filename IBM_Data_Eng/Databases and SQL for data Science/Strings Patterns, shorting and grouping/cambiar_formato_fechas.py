import pandas as pd

# Carga el archivo CSV sin encabezados
archivo_csv = '/home/erosennin/Programing/Visual Studio/Hands on Lab/Databases and SQL for data Science/Strings Patterns, shorting and grouping/JobsHistory.csv'  # Cambia esto a la ruta real del archivo CSV
column_names = ['emp_id', 'b_date', 'l_name','ssn']  # Nombres de las columnas

# Carga el archivo CSV y asigna nombres a las columnas
df = pd.read_csv(archivo_csv, header=None, names=column_names)

# Convierte el formato de las fechas
df['b_date'] = pd.to_datetime(df['b_date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')

# Guarda el DataFrame modificado en un nuevo archivo CSV
nuevo_archivo_csv = '/home/erosennin/Programing/Visual Studio/Hands on Lab/Databases and SQL for data Science/Strings Patterns, shorting and grouping/JobsHistory2.csv'
df.to_csv(nuevo_archivo_csv, index=False)
