FROM apache/airflow:2.6.2 

USER root
RUN apt-get update && apt-get install -y libgeos-dev

USER airflow
COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
