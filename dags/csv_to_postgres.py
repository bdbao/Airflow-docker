from datetime import datetime, timedelta
from urllib.parse import quote_plus

from module_connect.postgres import postgres_engine
import pandas as pd
import psycopg2
import pyodbc
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 9, 10),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def load_data_to_dataframe():
    path = "/opt/airflow/data/[rms].[E01OrderItems].csv"
    df = pd.read_csv(path, nrows=100)
    return df


def load_data_to_pgdb():
    df = load_data_to_dataframe()
    engine = create_engine(postgres_engine())
    df.to_sql(
        "E01OrderItems", engine, if_exists="append", schema="public", index=False
    )


with DAG(
    dag_id="CSV_to_Postgres_Pipeline",
    default_args=default_args,
    description="CSV to PostgreSQL",
    start_date=datetime(2023, 9, 10),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task1 = PythonOperator(task_id="first_task", python_callable=load_data_to_dataframe)

    task2 = PythonOperator(task_id="second_task", python_callable=load_data_to_pgdb)

    task1 >> task2
