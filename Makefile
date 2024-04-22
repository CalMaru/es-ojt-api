.DEFAULT_GOAL:=help

COMPOSE := -f docker-compose.yml

compose_v2_not_supported = $(shell command docker compose 2> /dev/null)
ifeq (,$(compose_v2_not_supported))
	DOCKER_COMPOSE_COMMAND = docker-compose
else
	DOCKER_COMPOSE_COMMAND = docker compose
endif

# --------------------------
.PHONY: ojt dev down stop help

ojt: ## Start ES-OJT container.
	@#echo "You can use 'make up dev=true' to run with development settings"
	$(DOCKER_COMPOSE_COMMAND) ${COMPOSE} up -d --build

down: ## Down ES-OJT container.
	$(DOCKER_COMPOSE_COMMAND) ${COMPOSE} down

stop: ## Stop ES-OJT container.
	$(DOCKER_COMPOSE_COMMAND) ${COMPOSE} stop

help: ## Show this help.
	@echo "Make Annotator with docker-compose files"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m (default: help)\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
