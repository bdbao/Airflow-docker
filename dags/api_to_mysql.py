from datetime import datetime, timedelta
from module_connect.mysql import mysql_engine
import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine
import requests

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 10, 26),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def collect_preprocess_data_api():
    # Link: https://rapidapi.com/apidojo/api/yh-finance/
    # url = 'https://yh-finance.p.rapidapi.com/market/v2/get-summary'
    url = 'https://yh-finance.p.rapidapi.com/auto-complete'

    # this is param in RapidAPI
    querystring = {
        "q": 'apple',
        "region": 'US'
    } 
    headers = {
        'X-RapidAPI-Key': '395434d0aamsh08cef3ad0561a05p125272jsn5df38f1f76ef',
        'X-RapidAPI-Host': 'yh-finance.p.rapidapi.com'
    }

    response = requests.get(url, headers=headers, params=querystring).json()
    df = pd.json_normalize(response['quotes'])

    return df


def load_data_to_mysql():
    df = collect_preprocess_data_api()
    df.to_sql(
        "yahooAutoComplete_quotes",
        create_engine(mysql_engine()),
        if_exists="replace", # or "append"
        index=False,
    )


with DAG(
    dag_id="API_to_MySQL_Pipeline",
    default_args=default_args,
    description="Get data from API to MySQL",
    start_date=datetime(2023, 10, 26),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task1 = PythonOperator(task_id="first_task", python_callable=collect_preprocess_data_api)

    task2 = PythonOperator(task_id="second_task", python_callable=load_data_to_mysql)

    task1 >> task2
