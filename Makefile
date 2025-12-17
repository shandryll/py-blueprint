PYTHON := python
MODULE := src.main

# Cria o ambiente virtual
venv:
	@echo "Criando ambiente virtual..."
	uv venv
	@echo "Ambiente virtual criado. Ative com: source .venv/bin/activate (Unix) ou .venv\\Scripts\\activate (Windows)"

# Instala dependências usando uv
install:
	@echo "Instalando dependências..."
	uv sync
	@echo "Dependências instaladas com sucesso!"

# Executa a aplicação
run:
	uv run python -m $(MODULE)

# Verifica linting
lint:
	uv run ruff check . --fix

# Formata o código
format:
	uv run ruff format .

# Executa testes
test:
	uv run pytest

# Limpa caches
clean:
	@echo "Limpando caches..."
	rm -rf .pytest_cache __pycache__ */__pycache__ *.pyc

.PHONY: venv install run lint format test clean
