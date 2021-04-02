FASTAPI=fastapi
RUN_IN_CONTAINER=docker-compose run --rm -u `id -u`:`id -u`
HIDE_DOCKER_CLI_DETAILES=COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1

build:
	$(HIDE_DOCKER_CLI_DETAILES) docker-compose build

init_db:
	docker-compose up -d postgres
	$(RUN_IN_CONTAINER) $(FASTAPI) python -m scripts.init_test_data
	docker exec -it `docker ps -aqf "name=postgres"` psql -U postgres -c "create user datadog with password 'datadog';"
	docker exec -it `docker ps -aqf "name=postgres"` psql -U postgres -c "grant pg_monitor to datadog;"
	docker exec -it `docker ps -aqf "name=postgres"` psql -U postgres -c "grant SELECT ON pg_stat_database to datadog;"
	docker-compose stop postgres

up:
	docker-compose up -d  --remove-orphans

down:
	docker-compose down

restart: down build up

logs:
	docker-compose logs -f

clean_volumes:
	docker-compose down --volumes