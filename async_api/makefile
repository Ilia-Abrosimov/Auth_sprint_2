start_all:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d

init_dbs:
	docker-compose exec redis redis-cli flushdb
	docker-compose exec etl sh ./preload.sh

start_tests:
	docker-compose -f tests/functional/docker-compose.yml up --build -d
