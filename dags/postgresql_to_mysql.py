from datetime import datetime, timedelta
from module_connect.postgres import connect_postgres
from module_connect.mysql import mysql_engine
import pandas as pd
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
def extract_data_from_pgdb():
    conn = connect_postgres()
    # SELECT * FROM Schema."Table" (We already specify Database in connection)
    query = """ SELECT "InvoiceNo",
                  "StockCode",
                  "Description",
                  "Quantity",
                  "InvoiceDate",
                  "UnitPrice",
                  "CustomerID",
                  "Country" FROM airflow."Invoice" """
    df = pd.read_sql(query, conn) 
    
    return df


# define function load data to Postgres Database
def load_data_to_mysql():
    df = extract_data_from_pgdb()
    engine = create_engine(mysql_engine())

    df.to_sql(
        "Invoice_fromPostgreSQL", engine, if_exists="append", index=False
    )


with DAG(
    dag_id="PostgreSQL_to_MySQL_Pipeline",
    default_args=default_args,
    description="Update PostgreSQL to MySQL",
    start_date=datetime(2023, 9, 10),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task1 = PythonOperator(
        task_id="load_data_from_postgres", python_callable=extract_data_from_pgdb
    )

    task2 = PythonOperator(task_id="load_data_to_mysql", python_callable=load_data_to_mysql)

    task1 >> task2
