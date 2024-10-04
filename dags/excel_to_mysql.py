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
    path = "/opt/airflow/data/[rms].[E00OrderType].xlsx"
    df = pd.read_excel(path, sheet_name="_rms_ _E00OrderType_", nrows=50)
    return df


def load_data_to_mysql():
    df = load_data_to_dataframe()
    df.to_sql(
        "E00OrderType",
        create_engine(mysql_engine()),
        if_exists="replace", # or "append"
        index=False,
    )


with DAG(
    dag_id="EXCEL_to_MySQL_Pipeline",
    default_args=default_args,
    description="Update Excel file to MySQL",
    start_date=datetime(2023, 10, 26),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task1 = PythonOperator(task_id="first_task", python_callable=load_data_to_dataframe)

    task2 = PythonOperator(task_id="second_task", python_callable=load_data_to_mysql)

    task1 >> task2
