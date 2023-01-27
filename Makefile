COMPOSE_RUNNER ?= COMPOSE_DOCKER_CLI_BUILD=1 docker-compose -f docker-compose.test.yml  run pytest


test:
	pytest -vv --tb=native tests/

compose-test:
	$(COMPOSE_RUNNER) make test