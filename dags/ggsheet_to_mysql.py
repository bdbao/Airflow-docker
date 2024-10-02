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


# extract data from ggsheet
def extract_data_from_ggsheet():
    googlesheetID = "15ZEKDLO3t5Ag-EeAD93PxxDhRoiygEpd_TWwpn9LXfc"
    worksheet = "728181631"
    myURL = "https://docs.google.com/spreadsheets/d/{0}/export?gid={1}&format=csv".format(
        googlesheetID, worksheet
    )
    df = pd.read_csv(myURL)
    return df


# define function load data to Mysql Database
def load_data_to_mysql():
    df = extract_data_from_ggsheet()
    df.to_sql(
        "E00Status",
        create_engine(mysql_engine()),
        if_exists="replace", # or "append"
        index=False,
    )


with DAG(
    dag_id="GGSheet_to_MySQL_Pipeline",
    default_args=default_args,
    description="Update GGSheet to MySQL",
    start_date=datetime(2023, 10, 26),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task1 = PythonOperator(task_id="first_task", python_callable=extract_data_from_ggsheet)

    task2 = PythonOperator(task_id="second_task", python_callable=load_data_to_mysql)

    task1 >> task2
