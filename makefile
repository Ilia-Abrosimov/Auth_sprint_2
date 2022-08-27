start_auth:
	docker-compose -f docker-compose.yml up --build -d

start_auth_dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d
