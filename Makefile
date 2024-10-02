CONTAINER_NAME = airflow-docker
POSTGRES_NAME = postgresql@16

start:
	echo "Starting $(POSTGRES_NAME) and container $(airflow-docker)..."
	brew services start postgresql@16
	docker start $(shell docker ps -q --filter "name=$(CONTAINER_NAME)")

stop:
	echo "Stopping $(POSTGRES_NAME) and container $(airflow-docker)..."
	brew services stop $(POSTGRES_NAME)
	docker stop $(shell docker ps -q --filter "name=$(CONTAINER_NAME)")

restart:
	echo "Restarting $(POSTGRES_NAME) and container $(airflow-docker)..."
	brew services restart $(POSTGRES_NAME)
	docker restart $(shell docker ps -a -q --filter "name=$(CONTAINER_NAME)")

renew:
	echo "Renewing Docker container..."
	docker compose down
	docker compose up -d

clean:
	rm -rdf logs/*

.PHONY: start stop restart renew clean