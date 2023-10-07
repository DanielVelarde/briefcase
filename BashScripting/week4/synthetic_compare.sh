#!/bin/bash
# Este script realiza cálculos sobre un archivo y muestra los resultados.

# Extrae la sexta columna de las últimas 7 líneas del archivo synthetic_historical_fc_accuracy.tsv y la guarda en scratch.txt
echo $(tail -7 synthetic_historical_fc_accuracy.tsv | cut -f6) > scratch.txt

# Lee los valores del archivo scratch.txt en un array llamado week_fc
week_fc=($(echo $(cat scratch.txt)))

# Imprime los valores del array week_fc (Validación)
echo "Valores originales del array week_fc:"
for i in {0..6}; do
    echo ${week_fc[$i]}
done

# Convierte los valores negativos en positivos en el array week_fc
for i in {0..6}; do
  if [[ ${week_fc[$i]} -lt 0 ]]; then
    week_fc[$i]=$(((-1)*${week_fc[$i]}))
  fi
  # Imprime los valores del array después de la conversión (Validación)
  echo "Valores del array week_fc después de la conversión:"
  echo ${week_fc[$i]}
done

# Encuentra el valor mínimo y máximo en el array week_fc
minimum=${week_fc[1]}
maximum=${week_fc[1]}
for item in ${week_fc[@]}; do
   if [[ $minimum -gt $item ]]; then
     minimum=$item
   fi
   if [[ $maximum -lt $item ]]; then
     maximum=$item
   fi
done

# Imprime el valor mínimo y máximo calculado
echo "Error absoluto mínimo = $minimum"
echo "Error absoluto máximo = $maximum"

