# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Daniel',
    'start_date': days_ago(0),
    'email': ['daniel.velarde.kubber@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG

# define the DAG
dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)
# define the task 'download & Unzip'

unzip_data_task = BashOperator(
    task_id='unzip_data',
    bash_command='wget -O /home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata.tgz "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz" && '
                 'tar -xzvf /home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata.tgz -C /home/erosennnin/Programing/Apache_Airflow/finalassignment/ && '
                 'ls /home/erosennnin/Programing/Apache_Airflow/finalassignment/',
    dag=dag,
)

# Create a BashOperator task to extract data from the CSV file
extract_data_task = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -d "," -f 1,2,3,4 /home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata/vehicle-data.csv > /home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata/csv_data.csv',
    dag=dag,
)

# Create a BashOperator task to extract data from the TSV file
extract_tsv_data_task = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -f5,6,7 /home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata/tollplaza-data.tsv > /home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata/tsv_data.csv',
    dag=dag,
)
# Create a BashOperator task to extract data from the fixed-width file
extract_fixed_width_data_task = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='cut -c1-4,12-13,16 /home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata/payment-data.txt > /home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata/fixed_width_data.csv',
    dag=dag,
)
# Create a BashOperator task to consolidate data from extracted files
consolidate_data_task = BashOperator(
    task_id='consolidate_data',
    bash_command='paste -d "," /home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata/csv_data.csv /home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata/tsv_data.csv /home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata/fixed_width_data.csv > /home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata/extracted_data.csv',
    dag=dag,
)

# Create a BashOperator task to transform the data
transform_data_task = BashOperator(
    task_id='transform_data',
    bash_command='tr "[a-z]" "[A-Z]" < //home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata/extracted_data.csv > /home/erosennnin/Programing/Apache_Airflow/finalassignment/tolldata/staging/transformed_data.csv',
    dag=dag,
)

# Task pipeline
unzip_data_task >> extract_data_task >> extract_tsv_data_task >> extract_fixed_width_data_task >> consolidate_data_task >> transform_data_task

