#!/bin/bash
echo "extract_transform_and_load"
cut -d":" -f1,3,6 /etc/passwd > /home/erosennnin/Programing/Apache_Airflow/Create_and_execute_a_Shell_script_from_Airflow/extracted-data.txt

tr ":" "," < /home/erosennnin/Programing/Apache_Airflow/Create_and_execute_a_Shell_script_from_Airflow/extracted-data.txt > /home/erosennnin/Programing/Apache_Airflow/Create_and_execute_a_Shell_script_from_Airflow/transformed-data.csv
