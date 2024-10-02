CONTAINER_NAME = airflow-docker
POSTGRES_NAME = postgresql@16
MYSQL_NAME = mysql

start:
	echo "Starting $(POSTGRES_NAME), $(MYSQL_NAME) and container $(airflow-docker)..."
	brew services start $(POSTGRES_NAME)
	brew services start $(MYSQL_NAME)
	docker start $(shell docker ps -a -q --filter "name=$(CONTAINER_NAME)")
	echo "Airflow is running at http://localhost:8080"

stop:
	echo "Stopping $(POSTGRES_NAME), $(MYSQL_NAME) and container $(airflow-docker)..."
	brew services stop $(POSTGRES_NAME)
	brew services stop $(MYSQL_NAME)
	docker stop $(shell docker ps -a -q --filter "name=$(CONTAINER_NAME)")

restart:
	echo "Restarting $(POSTGRES_NAME) and container $(airflow-docker)..."
	brew services restart $(POSTGRES_NAME)
	brew services restart $(MYSQL_NAME)
	docker restart $(shell docker ps -a -q --filter "name=$(CONTAINER_NAME)")

renew:
	echo "Renewing Docker container..."
	docker compose down
	docker compose up -d

clean:
	rm -rdf logs/*

.PHONY: start stop restart renew clean
