# Demonstration tasks using Airflow on Docker
---
- [Demonstration tasks using Airflow on Docker](#demonstration-tasks-using-airflow-on-docker)
- [Quick Start](#quick-start)
- [Build from scratch](#build-from-scratch)
  - [Update Library](#update-library)
  - [Host Database server](#host-database-server)
    - [PostgreSQL server](#postgresql-server)
    - [MySQL server](#mysql-server)
    - [MongoDB server](#mongodb-server)
  - [Data Migration from MSSQL to Gooogle Cloud Platform](#data-migration-from-mssql-to-gooogle-cloud-platform)
  - [Manipulate on GUI](#manipulate-on-gui)
    - [Airflow UI](#airflow-ui)
    - [View database on DBeaver](#view-database-on-dbeaver)

# Quick Start
- Open **Docker Desktop**.
```bash
git clone https://github.com/bdbao/Airflow-docker
cd Airflow-docker

mkdir -p ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u) \nAIRFLOW_GID=0" > .env

# if updated requirements.txt: `docker compose down` -> delete all related images (command is bellow) -> run this command again.
docker build --no-cache . --tag extending_airflow:latest 

brew install postgresql@16 # or: postgresql
brew install mysql
make start

export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
initdb YOUR_ARBITRARY_PATH/postgresDB
psql postgres
    CREATE DATABASE db_airflow;
    CREATE USER user_airflow WITH PASSWORD '1234';
    ALTER USER user_airflow WITH SUPERUSER;
    \q
mysql -u root
    CREATE DATABASE db_airflow;
    CREATE USER 'user_airflow'@'localhost' IDENTIFIED BY 'admin@123';
    GRANT ALL PRIVILEGES ON *.* TO 'user_airflow'@'localhost' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    \q
```
- Open **http://localhost:8080**. (Default account was created with: User: **airflow** / Password: **airflow**)
- Open **DBeaver** to view databases.
  
Stopping all services by `make stop`.\
Delete all images relating to Airflow: `docker images | grep "airflow" | awk '{print $3}' | xargs docker rmi -f && docker image prune -f && docker rmi -f postgres:13 redis`.

# Build from scratch
```bash
mkdir Airlow-docker && cd Airlow-docker
```
- Fetching `docker-compose.yaml`
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.2/docker-compose.yaml'
```
- Initialize environment:
```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u) \nAIRFLOW_GID=0" > .env
```
- Open **Docker Desktop**.
- Initialize the database:
```bash
docker compose up airflow-init
```
- Running Airflow:
```bash
docker compose up -d
```
Open **http://localhost:8080**.
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
docker-compose up -d --no-deps --build airflow-webserver airflow-scheduler
```
- Modify the volume key to include the additional paths want to mount (at line 79):\
`- ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data`
- Run full Docker services
```bash
docker compose down
docker compose up -d

docker ps
docker exec -it CONTAINER_ID bash
```

## Host Database server
### PostgreSQL server
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

### MySQL server
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
### MongoDB server
Use [MongoDB Compass](https://www.mongodb.com/products/tools/compass).
```bash
show dbs

use db_airflow
db["Invoice_fromMySQL"].find()

# use admin
# db.grantRolesToUser("user_airflow", [{ role: "readWrite", db: "db_airflow" }])
```

## Data Migration from MSSQL to Gooogle Cloud Platform
1. Create a Google Cloud Project
- Go to [Google Cloud Console](https://console.cloud.google.com).
- Click **Select a Project** > **New Project**.
- Provide a project name and click **Create**.
2. Enable Required APIs
- In the **Cloud Console**, navigate to **APIs & Services > Library**.
- Enable the following APIs: **BigQuery API** and **Cloud Storage API**.
3. Create a Service Account (User Principal)
- Navigate to **IAM & Admin > Service Accounts**.
- Click **+ Create Service Account**.
- Provide a name (for example: *techdata-cloud @ zinc-union-443512-p7.iam.gserviceaccount.com*) for the service account and click **Create**.
- Assign the role **BigQuery Admin** (for full BigQuery management access).
- Click **Done**.
4. Generate and Save Service Account Key (JSON)
- Go back to **IAM & Admin > Service Accounts**.
- Select the service account you just created.
- Click **Keys > Add Key > Create New Key**.
- Select **JSON** format and download the file.
- Save the downloaded JSON file as: `./config/edtech.json`.
5. (Optional) Access airflow-containers bash:
    ```bash
    docker exec -u root -it airflow-docker-airflow-worker-1 bash # similarly with: webserver-1, scheduler-1
        apt-get install -y libgeos-dev
        # some more libs
    ```

## Manipulate on GUI
### Airflow UI
- Click **CSV_to_Postgres_Pipeline** in Airflow, then navigate to **Graph** -> Click on **Node** -> **Log** to view the output console.
- Re-run (Click **Play button** "Trigger DAG") once editting in `dags/` scripts.

### View database on DBeaver
Open **DBeaver** to view overall database PostgreSQL (by user_airflow), MySQL (by root, or user_airflow).

- Fix **Issue in DBeaver**: View MySQL db with user other than `root` \
    You need to enable public key retrieval by changing the connection settings.
    1. Step 1: Open DBeaver and go to your MySQL connection.
    2. Step 2: Click on **Edit Connection**.
    3. Step 3: Go to the **Driver Properties** tab.
    4. Step 4: Find or add the property **allowPublicKeyRetrieval** and set its value to **TRUE**.

<!-- 
## More more
- Reinstall requirements.txt:
```bash
docker compose down --volumes
docker compose build
docker compose up -d

docker exec -it airflow-docker-airflow-webserver-1 bash
    python -c "import pymongo; print('pymongo is installed successfully')"
``` 
-->
