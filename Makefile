init:
	cp .env.dist .env
	cp django_admin/.env.dist django_admin/.env
	cp postgres_to_es/.env.dist postgres_to_es/.env
	cp fastapi_api/.env.dist fastapi_api/.env
	cp auth_service/api/.env.dist auth_service/api/.env
	cp auth_service/grpc/.env.dist auth_service/grpc/.env

	$(MAKE) down
	$(MAKE) build
	$(MAKE) up

	docker exec -it django_admin_app make django-migrate
	docker exec -it django_admin_app make admin
	docker exec -it django_admin_app make sqlite-load
	docker exec -it auth_grpc_app make alembic-migrate
	docker exec -it auth_grpc_app make policy
	docker exec -it auth_grpc_app make admin

	docker restart postgres_to_es_app  # force restart etl, stuck cause of invalid schema :kostyl:

build:
	docker-compose --env-file $$(cat ".env" "./django_admin/.env" "./postgres_to_es/.env" "./fastapi_api/.env" "./auth_service/grpc/.env" "./auth_service/api/.env" > merged.env && echo merged.env) build --parallel
down:
	docker-compose --env-file $$(cat ".env" "./django_admin/.env" "./postgres_to_es/.env" "./fastapi_api/.env" "./auth_service/grpc/.env" "./auth_service/api/.env" > merged.env && echo merged.env) down --volumes
up:
	docker-compose --env-file $$(cat ".env" "./django_admin/.env" "./postgres_to_es/.env" "./fastapi_api/.env" "./auth_service/grpc/.env" "./auth_service/api/.env" > merged.env && echo merged.env) up -d

test_fastapi:
	cp fastapi_api/tests/functional/.env.dist fastapi_api/tests/functional/.env
	docker-compose -f docker/docker-compose.fastapi.test.yml --env-file ./fastapi_api/tests/functional/.env down --volumes
	docker-compose -f docker/docker-compose.fastapi.test.yml --env-file ./fastapi_api/tests/functional/.env build
	docker-compose -f docker/docker-compose.fastapi.test.yml --env-file ./fastapi_api/tests/functional/.env up --abort-on-container-exit --exit-code-from tests

test_auth:
	cp auth_service/tests/functional/.env.dist auth_service/tests/functional/.env
	docker-compose -f docker/docker-compose.auth.test.yml --env-file ./auth_service/tests/functional/.env down --volumes
	docker-compose -f docker/docker-compose.auth.test.yml --env-file ./auth_service/tests/functional/.env build
	docker-compose -f docker/docker-compose.auth.test.yml --env-file ./auth_service/tests/functional/.env up --abort-on-container-exit --exit-code-from tests

lint:
	pre-commit run --all-files
