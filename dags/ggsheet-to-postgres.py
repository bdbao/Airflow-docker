from datetime import datetime, timedelta
from module_connect.postgres import postgres_engine
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

def load_data_to_pgdb():
    df = extract_data_from_ggsheet()
    engine = create_engine(postgres_engine())
    df.to_sql("E00Status", engine, if_exists="replace", schema="public", index=False)


with DAG(
    dag_id="GGSheet_to_Postgres_Pipeline",
    default_args=default_args,
    description="Update GGSheet to Postgres",
    start_date=datetime(2023, 10, 26),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task1 = PythonOperator(
        task_id="load_data_from_ggsheet", python_callable=extract_data_from_ggsheet
    )

    task2 = PythonOperator(task_id="load_data_to_db_postgres", python_callable=load_data_to_pgdb)

    task1 >> task2
