from datetime import datetime, timedelta
from urllib.parse import quote_plus

from module_connect.mysql import connect_mysql
from module_connect.postgres import postgres_engine
import mysql.connector
import pymysql
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


# extract data from sql server
def extract_data_from_mysql():
    conn = connect_mysql()
    query = """SELECT id, madonhang, ngaydat, masanpham, slban, dongia,
    				doanhthu, trangthaidonghang
    			FROM sales.fact_sales;"""
    df = pd.read_sql(query, conn)
    return df


# define function load data to Postgres Database
def load_data_to_pgdb():
    df = extract_data_from_mysql()
    engine = create_engine(postgres_engine())
    df.to_sql(
        "fact_sales", engine, if_exists="append", schema="public", index=False
    )


with DAG(
    dag_id="MySQL_to_Postgres_Pipeline",
    default_args=default_args,
    description="Update MySQL to PostgreSQL",
    start_date=datetime(2023, 9, 10),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task1 = PythonOperator(
        task_id="load_data_from_mysql", python_callable=extract_data_from_mysql
    )

    task2 = PythonOperator(task_id="load_data_to_postgres", python_callable=load_data_to_pgdb)

    task1 >> task2
