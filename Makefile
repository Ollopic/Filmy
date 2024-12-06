help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: docs

init: ## init project
	@docker compose down -v
	@$(MAKE) start
	@$(MAKE) log

start: ## start containers
	@docker compose up -d --build

stop: ## stop containers
	@docker compose stop

restart: ## restart containers
	@docker compose restart

log: ## log web and back containers
	@docker compose logs -f --tail 100

log-web: ## log web container
	@docker compose logs -f --tail 100 web

log-back: ## log back container
	@docker compose logs -f --tail 100 backend