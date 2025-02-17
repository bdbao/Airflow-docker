from datetime import datetime, timedelta
from module_connect.mongodb import connect_mongodb
from module_connect.mysql import mysql_engine
import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 1, 10),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Extract data from MongoDB
def extract_data_from_mongodb():
    db = connect_mongodb()
    collection = db["Invoice_fromMySQL"]  # Replace with your MongoDB collection name
    data = list(collection.find({}, {"_id": 0}))  # Exclude _id field
    df = pd.DataFrame(data)
    return df

# Load data into MySQL
def load_data_to_mysql():
    df = extract_data_from_mongodb()
    engine = create_engine(mysql_engine())
    df.to_sql("Invoice_fromMongoDB", engine, if_exists="append", index=False)

with DAG(
    dag_id="MongoDB_to_MySQL_Pipeline",
    default_args=default_args,
    description="Update MongoDB to MySQL",
    start_date=datetime(2023, 9, 10),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    task1 = PythonOperator(
        task_id="load_data_from_mongodb", python_callable=extract_data_from_mongodb
    )

    task2 = PythonOperator(
        task_id="load_data_to_mysql", python_callable=load_data_to_mysql
    )

    task1 >> task2
