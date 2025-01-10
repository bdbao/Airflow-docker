from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from sqlalchemy import create_engine
from google.cloud import bigquery
import pandas as pd

# SQL Server connection URI
SQL_SERVER_URI = "mssql+pyodbc://SA:Admin%40123@host.docker.internal:1433/RestoreDW?driver=ODBC+Driver+18+for+SQL+Server&encrypt=no"

# BigQuery settings
BIGQUERY_PROJECT = "zinc-union-443512-p7"
BIGQUERY_DATASET = "EDW_Tech_2022"
TABLE_NAME = "ecom_E00Target" # Edit table name here!
BIGQUERY_LOCATION = "US" 

# Extract data from SQL Server
def extract_data_from_sqlserver():
    engine = create_engine(SQL_SERVER_URI)
    try:
        query = "SELECT * FROM [ecom].[E00Target]"
        df = pd.read_sql_query(query, con=engine)
        print(f"Data extracted from table {TABLE_NAME}")
        return df
    except Exception as e:  
        print(f"Failed to extract data from table {TABLE_NAME}: {e}")
        return None

# Create BigQuery Dataset if not exists
def create_bigquery_dataset():
    client = bigquery.Client(project=BIGQUERY_PROJECT)
    dataset_ref = bigquery.DatasetReference(BIGQUERY_PROJECT, BIGQUERY_DATASET)
    try:
        client.get_dataset(dataset_ref)  # Check if dataset exists
        print(f"Dataset {BIGQUERY_DATASET} already exists.")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = BIGQUERY_LOCATION
        client.create_dataset(dataset, exists_ok=True)
        print(f"Dataset {BIGQUERY_DATASET} created successfully in {BIGQUERY_LOCATION}")

# Load data to BigQuery
def load_data_to_bigquery(**context):
    data = context['ti'].xcom_pull(task_ids='extract_data_from_sqlserver')
    
    if data is not None:
        client = bigquery.Client(project=BIGQUERY_PROJECT)
        table_id = f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.{TABLE_NAME}"
        
        try:
            # Cấu hình job
            job_config = bigquery.LoadJobConfig(
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE # Ghi de du lieu cu
            )
            job = client.load_table_from_dataframe(data, table_id, job_config=job_config)
            job.result()
            print(f"Table {TABLE_NAME} loaded successfully to {table_id}.")
        except Exception as e:
            print(f"Failed to load data into table {TABLE_NAME}: {e}")
    else:
        print("No data available to load into BigQuery.")

# Check SQL Server connection
def check_sqlserver_connection():
    engine = create_engine(SQL_SERVER_URI)
    try:
        with engine.connect() as connection:
            print("Connected to SQL Server successfully!")
    except Exception as e:
        raise RuntimeError(f"Failed to connect to SQL Server: {e}")

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id='mssql_to_bigquery_single_table',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    # Task to check SQL Server connection
    check_connection = PythonOperator(
        task_id='check_sqlserver_connection',
        python_callable=check_sqlserver_connection,
    )

    # Task to create the dataset if not exists
    create_dataset = PythonOperator(
        task_id='create_bigquery_dataset',
        python_callable=create_bigquery_dataset,
    )

    # Task to extract data from SQL Server
    extract_data = PythonOperator(
        task_id='extract_data_from_sqlserver',
        python_callable=extract_data_from_sqlserver,
    )

    # Task to load data into BigQuery
    load_table = PythonOperator(
        task_id='load_data_to_bigquery',
        python_callable=load_data_to_bigquery,
        provide_context=True,
    )

    # Set task dependencies
    check_connection >> create_dataset >> extract_data >> load_table
