PYTHON := python
MODULE := src.main

# Cria o ambiente virtual
venv:
	@echo "Criando ambiente virtual..."
	uv venv
	@echo "Ambiente virtual criado. Use 'uv run ...' para executar comandos no venv."

# Instala dependências de runtime + dev
install-dev:
	@echo "Instalando dependências (incluindo dev)..."
	uv sync --dev --extra dev
	@echo "Dependências instaladas com sucesso!"

# Instala apenas dependências de produção
install-prod:
	@echo "Instalando dependências de produção..."
	uv sync
	@echo "Dependências de produção instaladas com sucesso!"

# Executa a aplicação
run:
	uv run uvicorn $(MODULE):app --reload

# Verifica linting
lint:
	uv run ruff check . --fix

# Formata o código
format:
	uv run ruff format .

# Executa testes
test:
	uv run pytest -s -v

# Executa testes com cobertura
test-cov:
	uv run pytest --cov=src --cov-report=html --cov-report=term -s -v

# Limpa caches
clean:
	@echo "Limpando caches..."
	rm -rf .pytest_cache __pycache__ */__pycache__ *.pyc
	rm -rf .coverage htmlcov/ coverage.xml
	rm -rf build/ dist/ *.egg-info

# Docker commands
docker-build:
	docker build -t py-blueprint .

docker-run:
	docker-compose up -d

docker-logs:
	docker-compose logs -f

docker-stop:
	docker-compose down

docker-clean:
	docker-compose down -v
	docker rmi py-blueprint 2>/dev/null || true

# Instala hooks de pre-commit
pre-commit-install:
	@echo "Instalando pre-commit..."
	uv run pip install pre-commit
	pre-commit install
	@echo "Pre-commit instalado e hooks configurados."

.PHONY: venv install-dev install-prod dev run lint format test test-cov clean pre-commit-install docker-build docker-run docker-logs docker-stop docker-clean
