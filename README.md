```bash
cd Airlow-docker
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.2/docker-compose.yaml'
```
- Initialize environment:
```bash
mkdir -p ./dags ./logs ./plugins ./config
```
1. Setting the right user (optional): 
```bash
echo -e "AIRFLOW_UID=$(id -u) \nAIRFLOW_GID=0" > .env
```
- Initialize the database:
```bash
docker compose up airflow-init
```
- Running Airflow:
```bash
docker compose up -d
```
Open **http://localhost:8080**

(Default account was created with: **User**: airflow / **Password**: airflow)

## Update Library
- Create Dockerfile
- Change in `docker-compose.yaml` like this:
    ```
    # image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.6.2}
    build: .
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    ```
- Build the extended image by command
```bash
docker build . --tag extending_airflow:latest
```
```bash
docker-compose up -d --no-deps --build airflow-webserver airflow-scheduler
```
- Modify the volume key to include the additional paths want to mount (at line 79)
  ```
  - ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data
  ```
- Run full Docker services
```bash
docker compose down
docker compose up -d
```

## Host Postgres server
```bash
brew install postgresql
brew services start postgresql@16 # (or postgresql)
(brew services stop postgresql@16)
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
initdb YOUR_ARBITRARY_PATH/postgresDB

psql postgres
    \l # list all db
    CREATE DATABASE db_airflow;
    
    # delete db
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = 'your_db';
    DROP DATABASE your_db;

    \du # list all users
    # add new user
    CREATE USER user_airflow WITH PASSWORD '1234';
    ALTER USER user_airflow WITH SUPERUSER; # (optional)
    
    # delete user
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.usename = 'username_to_delete';
    DROP USER username_to_delete;

    # change password
    ALTER USER your_username WITH PASSWORD 'new_password';

    \q # quit psql postgres
```

Click **CSV_to_Postgres_Pipeline** in Airflow, then navigate to **Graph** -> Click on **Node** -> **Log** to view the output console.
Re-run once editting in `dags/` scripts.