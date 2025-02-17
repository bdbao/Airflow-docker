from datetime import datetime, timedelta
from module_connect.mysql import connect_mysql
from module_connect.mongodb import connect_mongodb
import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 12, 30),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# extract data from MySQL
def extract_data_from_mysql():
    conn = connect_mysql()
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

# load data into MongoDB
def load_data_to_mongodb():
    df = extract_data_from_mysql()
    db = connect_mongodb()
    collection = db["Invoice_fromMySQL"]

    # Convert DataFrame to a list of dictionaries and insert into MongoDB
    data = df.to_dict(orient="records")
    collection.insert_many(data)

with DAG(
    dag_id="MySQL_to_MongoDB_Pipeline",
    default_args=default_args,
    description="Update MySQL to MongoDB",
    start_date=datetime(2024, 12, 30),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    task1 = PythonOperator(
        task_id="extract_data_from_mysql", python_callable=extract_data_from_mysql
    )

    task2 = PythonOperator(
        task_id="load_data_to_mongodb", python_callable=load_data_to_mongodb
    )

    task1 >> task2
