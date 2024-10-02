from datetime import datetime, timedelta
from module_connect.mysql import connect_mysql
from module_connect.postgres import postgres_engine
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
def extract_data_from_mysql():
    conn = connect_mysql()
    # SELECT * FROM Table (We already specify Database in connection)
    query = """ SELECT InvoiceNo,
                    StockCode,
                    Description,
                    Quantity,
                    InvoiceDate,
                    UnitPrice,
                    CustomerID,
                    Country FROM Invoice; """
    df = pd.read_sql(query, conn) 
    return df


# define function load data to Postgres Database
def load_data_to_pgdb():
    df = extract_data_from_mysql()
    engine = create_engine(postgres_engine())

    with engine.connect() as conn:
        conn.execute("CREATE SCHEMA IF NOT EXISTS airflow;")

    df.to_sql(
        "Invoice_fromMySQL", engine, if_exists="append", schema="airflow", index=False
    )


with DAG(
    dag_id="MySQL_to_PostgreSQL_Pipeline",
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
