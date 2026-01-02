.PHONY: help build up down restart logs shell test clean

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Constrói a imagem Docker
	docker-compose build

up: ## Inicia os containers em modo desenvolvimento
	docker-compose up -d

up-build: ## Constrói e inicia os containers
	docker-compose up --build -d

down: ## Para e remove os containers
	docker-compose down

restart: ## Reinicia os containers
	docker-compose restart

logs: ## Mostra os logs dos containers
	docker-compose logs -f api

shell: ## Abre um shell no container
	docker-compose exec api /bin/bash

test: ## Executa todos os testes
	@python run_tests.py

test-state: ## Executa testes do State pattern
	@python src/behavioral/state/test_state.py

test-strategy: ## Executa testes do Strategy pattern
	@python src/behavioral/strategy/test_strategy.py

test-observer: ## Executa testes do Observer pattern
	@python src/behavioral/observer/test_observer.py

test-template: ## Executa testes do Template Method pattern
	@python src/behavioral/template_method/test_template_method.py

test-adapter: ## Executa testes do Adapter pattern
	@python src/structural/adapter/test_adapter.py

test-decorator: ## Executa testes do Decorator pattern
	@python src/structural/decorator/test_decorator.py

test-facade: ## Executa testes do Facade pattern
	@python src/structural/facade/test_facade.py

clean: ## Remove containers, volumes e imagens
	docker-compose down -v --rmi all

prod-build: ## Constrói para produção
	docker-compose -f docker-compose.prod.yml build

prod-up: ## Inicia em modo produção
	docker-compose -f docker-compose.prod.yml up -d

prod-down: ## Para produção
	docker-compose -f docker-compose.prod.yml down

prod-logs: ## Logs de produção
	docker-compose -f docker-compose.prod.yml logs -f

