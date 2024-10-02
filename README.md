# Demo Airflow tasks on Docker
- Fetching `docker-compose.yaml`
```bash
cd Airlow-docker
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.2/docker-compose.yaml'
```
- Initialize environment:
```bash
mkdir -p ./dags ./logs ./plugins ./config
```
Setting the right user (optional): 
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

(Default account was created with: User: **airflow** / Password: **airflow**)

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

docker ps
docker exec -it CONTAINER_ID bash
```

## Host PostgreSQL server
```bash
brew install postgresql
brew services start postgresql@16 # (or postgresql)
(brew services stop postgresql@16)
brew services list

export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
initdb YOUR_ARBITRARY_PATH/postgresDB

psql postgres
    \l # list all db

    # create db
    CREATE DATABASE db_airflow;
    
    # delete db
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = 'your_db';
    DROP DATABASE your_db;

    # list all users
    \du 

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

## Host MySQL server
```bash
brew install mysql
brew services start mysql
(brew services stop mysql)
brew services list

mysql -u root
mysql -u root -p # if you’ve set a password
    # list all db
    SHOW DATABASES; 
    
    # create db
    CREATE DATABASE db_airflow;

    USE db_airflow;
    SHOW TABLES;
    SELECT * FROM table_name;

    # delete db
    DROP DATABASE db_airflow;

    # list all users
    SELECT User, Host FROM mysql.user;
    SHOW GRANTS FOR 'root'@'localhost'; # show user privileges
 
    # add new user
    CREATE USER 'user_airflow'@'localhost' IDENTIFIED BY 'admin@123'; # (use % for any host)
    GRANT ALL PRIVILEGES ON *.* TO 'user_airflow'@'localhost'; # (optional)
    GRANT ALL PRIVILEGES ON *.* TO 'user_airflow'@'localhost' WITH GRANT OPTION;
    FLUSH PRIVILEGES; # apply changes
    SHOW GRANTS FOR 'user_airflow'@'%';

    # delete user
    DROP USER 'user_airflow'@'localhost';

    # change password
    ALTER USER 'username'@'host' IDENTIFIED BY 'new_password';
    FLUSH PRIVILEGES;

    \q # quit mysql
```
## Manipulate on Airflow GUI
Click **CSV_to_Postgres_Pipeline** in Airflow, then navigate to **Graph** -> Click on **Node** -> **Log** to view the output console.\
Re-run (Click **Play button** "Trigger DAG") once editting in `dags/` scripts.

## View database on DBeaver
Open **DBeaver** to view overall database PostgreSQL (by user_airflow), MySQL (by root, or user_airflow).

### Fix the Issue in DBeaver (for MySQL with user other than `root`)
You need to enable public key retrieval by changing the connection settings.
1. Step 1: Open DBeaver and go to your MySQL connection.
2. Step 2: Click on **Edit Connection**.
3. Step 3: Go to the **Driver Properties** tab.
4. Step 4: Find or add the property **allowPublicKeyRetrieval** and set its value to **true**.
