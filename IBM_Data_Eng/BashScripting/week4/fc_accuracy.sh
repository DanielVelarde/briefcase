#!/bin/bash
# Este script calcula la precisión de un pronóstico meteorológico y registra los resultados en un archivo TSV.

# Obtener el pronóstico de ayer desde la penúltima línea del archivo rx_poc.log
yesterday_fc=$(tail -2 rx_poc.log | head -1 | cut -d " " -f5)

# Obtener la temperatura de hoy desde la última línea del archivo rx_poc.log
today_temp=$(tail -1 rx_poc.log | cut -d " " -f4)

# Calcular la diferencia de precisión entre el pronóstico de ayer y la temperatura de hoy
accuracy=$(($yesterday_fc - $today_temp))

# Imprimir la precisión calculada
echo "Precisión calculada: $accuracy"

# Determinar la categoría de precisión en función de la diferencia calculada
if [ -1 -le $accuracy ] && [ $accuracy -le 1 ]; then
    accuracy_range="Excelente"
elif [ -2 -le $accuracy ] && [ $accuracy -le 2 ]; then
    accuracy_range="Buena"
elif [ -3 -le $accuracy ] && [ $accuracy -le 3 ]; then
    accuracy_range="Regular"
else
    accuracy_range="Pobre"
fi

# Imprimir la categoría de precisión
echo "Categoría de precisión: $accuracy_range"

# Extraer la fecha de la última línea de rx_poc.log
row=$(tail -1 rx_poc.log)
year=$(echo $row | cut -d " " -f1)
month=$(echo $row | cut -d " " -f2)
day=$(echo $row | cut -d " " -f3)

# Imprimir la fecha extraída
echo "Fecha: $year-$month-$day"

# Guardar los resultados en un archivo TSV llamado historical_fc_accuracy.tsv
echo -e "$year\t$month\t$day\t$today_temp\t$yesterday_fc\t$accuracy\t$accuracy_range" >> historical_fc_accuracy.tsv

# Fin del script

