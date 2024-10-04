from datetime import datetime, timedelta
from module_connect.mysql import mysql_engine
import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 10, 26),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def load_data_to_dataframe():
    path = "/opt/airflow/data/data.csv"
    df = pd.read_csv(path, nrows=100)
    return df


def load_data_to_mysql():
    df = load_data_to_dataframe()
    df.to_sql(
        "Invoice",
        create_engine(mysql_engine()),
        if_exists="replace", # or "append"
        index=False,
    )


with DAG(
    dag_id="CSV_to_MySQL_Pipeline",
    default_args=default_args,
    description="Update CSV file to MySQL",
    start_date=datetime(2023, 10, 26),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task1 = PythonOperator(task_id="first_task", python_callable=load_data_to_dataframe)

    task2 = PythonOperator(task_id="second_task", python_callable=load_data_to_mysql)

    task1 >> task2
