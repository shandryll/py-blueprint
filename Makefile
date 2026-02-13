# =============================================================================
# Makefile para py-blueprint - Template Python/FastAPI MVC
# =============================================================================

# Variáveis de configuração
PYTHON := python3
PROJECT_NAME := py-blueprint
PROJECT_VERSION := $(shell grep -E '^version\s*=' pyproject.toml | sed -E 's/.*version\s*=\s*"([^"]+)".*/\1/' || echo "dev")
MODULE := src.main
VENV_DIR := .venv

# Configurações da aplicação
HOST := 0.0.0.0
PORT := 8000

# Cores para output
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;36m
NC := \033[0m # No Color

# =============================================================================
# COMANDOS PRINCIPAIS
# =============================================================================
.PHONY: help
help: ## Mostra esta mensagem de ajuda
	@echo "$(BLUE)║===== $(PROJECT_NAME) - Makefile Helper =====║$(NC)"
	@echo ""
	@echo "$(YELLOW)🐍 AMBIENTE VIRTUAL:$(NC)"
	@echo ""
	@echo "$(GREEN)  make venv$(NC)         ## Cria ambiente virtual Python"
	@echo ""
	@echo "$(YELLOW)🚀 COMANDOS PRINCIPAIS (UV):$(NC)"
	@echo ""
	@echo "$(GREEN)  make setup$(NC)        ## Setup inicial completo (venv + install + pre-commit)"
	@echo "$(GREEN)  make install$(NC)      ## Instala dependências com uv"
	@echo "$(GREEN)  make run$(NC)          ## Executa a aplicação FastAPI com uv"
	@echo ""
	@echo "$(YELLOW)🚀 COMANDOS PRINCIPAIS (CLASSIC/PIP):$(NC)"
	@echo ""
	@echo "$(GREEN)  make setup-classic$(NC)     ## Setup inicial completo usando pip/venv tradicional"
	@echo "$(GREEN)  make install-classic$(NC)  ## Instala dependências com pip"
	@echo "$(GREEN)  make run-classic$(NC)      ## Executa a aplicação FastAPI com pip"
	@echo ""
	@echo "$(YELLOW)🔧 DESENVOLVIMENTO (UV):$(NC)"
	@echo ""
	@echo "$(GREEN)  make lint$(NC)         ## Verifica e corrige código com uv"
	@echo "$(GREEN)  make format$(NC)      ## Formata o código com uv"
	@echo "$(GREEN)  make test$(NC)        ## Executa testes com uv"
	@echo "$(GREEN)  make test-cov$(NC)    ## Executa testes com cobertura (uv)"
	@echo "$(GREEN)  make check$(NC)       ## Roda todas as verificações (lint + test) com uv"
	@echo ""
	@echo "$(YELLOW)🔧 DESENVOLVIMENTO (CLASSIC/PIP):$(NC)"
	@echo ""
	@echo "$(GREEN)  make lint-classic$(NC)     ## Verifica e corrige código com pip"
	@echo "$(GREEN)  make format-classic$(NC)   ## Formata o código com pip"
	@echo "$(GREEN)  make test-classic$(NC)     ## Executa testes com pip"
	@echo "$(GREEN)  make test-cov-classic$(NC) ## Executa testes com cobertura (pip)"
	@echo ""
	@echo "$(YELLOW)🐳 DOCKER:$(NC)"
	@echo ""
	@echo "$(GREEN)  make docker-build$(NC) ## Constrói imagem Docker"
	@echo "$(GREEN)  make docker-run$(NC)   ## Inicia containers Docker"
	@echo "$(GREEN)  make docker-logs$(NC)  ## Visualiza logs dos containers"
	@echo "$(GREEN)  make docker-stop$(NC)  ## Para containers Docker"
	@echo "$(GREEN)  make docker-clean$(NC) ## Remove containers e volumes"
	@echo ""
	@echo "$(YELLOW)🛡️  SEGURANÇA:$(NC)"
	@echo ""
	@echo "$(GREEN)  make security$(NC)     ## Verifica segurança do código e dependências"
	@echo ""
	@echo "$(YELLOW)🧹 LIMPEZA:$(NC)"
	@echo ""
	@echo "$(GREEN)  make clean$(NC)        ## Remove arquivos temporários e ambiente virtual"
	@echo ""

.PHONY: setup
setup: ## Setup inicial completo do projeto (usando uv)
	@echo "$(BLUE)🚀 Configurando projeto com uv...$(NC)"
	@echo ""
	@$(MAKE) venv
	@echo ""
	@$(MAKE) install
	@echo ""
	@$(MAKE) pre-commit-install
	@echo ""
	@echo "$(GREEN)✅ Setup completo!$(NC)"
	@echo "$(YELLOW)💡 Ative o ambiente virtual: source $(VENV_DIR)/bin/activate$(NC)"
	@echo "$(YELLOW)💡 Execute a aplicação: make run$(NC)"

.PHONY: setup-classic
setup-classic: ## Setup inicial completo do projeto (usando pip/venv tradicional)
	@echo "$(BLUE)🚀 Configurando projeto com pip/venv tradicional...$(NC)"
	@echo ""
	@$(MAKE) venv
	@echo ""
	@$(MAKE) install-classic
	@echo ""
	@echo "$(GREEN)✅ Setup completo!$(NC)"
	@echo "$(YELLOW)💡 Ative o ambiente virtual: source $(VENV_DIR)/bin/activate$(NC)"
	@echo "$(YELLOW)💡 Execute a aplicação: make run-classic$(NC)"

.PHONY: venv
venv: ## Cria ambiente virtual Python
	@echo "$(BLUE)Criando ambiente virtual...$(NC)"
	@$(PYTHON) -m venv $(VENV_DIR)
	@echo "$(GREEN)✅ Ambiente virtual criado!$(NC)"
	@echo "$(YELLOW)💡 Para ativar o ambiente virtual:$(NC)"
	@echo "$(YELLOW)   Linux/Mac: source $(VENV_DIR)/bin/activate$(NC)"
	@echo "$(YELLOW)   Windows: $(VENV_DIR)\\Scripts\\activate$(NC)"

.PHONY: install
install: ## Instala dependências do projeto (usando uv)
	@echo "$(BLUE)Instalando dependências com uv...$(NC)"
	@uv sync --dev --extra dev --python python3
	@echo "$(GREEN)✅ Dependências instaladas!$(NC)"

.PHONY: install-classic
install-classic: ## Instala dependências do projeto (usando pip/venv tradicional)
	@echo "$(BLUE)Instalando dependências com pip...$(NC)"
	@pip install --upgrade pip
	@pip install -r requirements/dev.txt
	@echo "$(GREEN)✅ Dependências instaladas!$(NC)"

.PHONY: pre-commit-install
pre-commit-install: ## Instala hooks do pre-commit
	@echo "$(BLUE)Instalando hooks do pre-commit...$(NC)"
	@uv run pre-commit install
	@echo "$(GREEN)✅ Pre-commit configurado!$(NC)"

.PHONY: run
run: ## Executa a aplicação FastAPI (usando uv)
	@echo "$(BLUE)Iniciando aplicação com uv...$(NC)"
	@echo "$(YELLOW)💡 Documentação: http://$(HOST):$(PORT)/docs$(NC)"
	@echo ""
	@uv run uvicorn $(MODULE):app --host $(HOST) --port $(PORT) --reload

.PHONY: run-classic
run-classic: ## Executa a aplicação FastAPI (usando pip/venv tradicional)
	@echo "$(BLUE)Iniciando aplicação com pip/venv tradicional...$(NC)"
	@echo "$(YELLOW)💡 Documentação: http://$(HOST):$(PORT)/docs$(NC)"
	@echo ""
	@uvicorn $(MODULE):app --host $(HOST) --port $(PORT) --reload

.PHONY: lint
lint: ## Verifica e corrige código (usando uv)
	@echo "$(BLUE)Verificando código com uv...$(NC)"
	@uv run ruff check . --fix
	@echo "$(GREEN)✅ Verificação concluída!$(NC)"

.PHONY: lint-classic
lint-classic: ## Verifica e corrige código (usando pip/venv tradicional)
	@echo "$(BLUE)Verificando código com pip...$(NC)"
	@ruff check . --fix
	@echo "$(GREEN)✅ Verificação concluída!$(NC)"

.PHONY: format
format: ## Formata o código (usando uv)
	@echo "$(BLUE)Formatando código com uv...$(NC)"
	@uv run ruff format .
	@echo "$(GREEN)✅ Formatação concluída!$(NC)"

.PHONY: format-classic
format-classic: ## Formata o código (usando pip/venv tradicional)
	@echo "$(BLUE)Formatando código com pip...$(NC)"
	@ruff format .
	@echo "$(GREEN)✅ Formatação concluída!$(NC)"

.PHONY: test
test: ## Executa testes (usando uv)
	@echo "$(BLUE)Executando testes com uv...$(NC)"
	@uv run pytest -s -v
	@echo "$(GREEN)✅ Testes concluídos!$(NC)"

.PHONY: test-classic
test-classic: ## Executa testes (usando pip/venv tradicional)
	@echo "$(BLUE)Executando testes com pip...$(NC)"
	@pytest -s -v
	@echo "$(GREEN)✅ Testes concluídos!$(NC)"

.PHONY: test-cov
test-cov: ## Executa testes com relatório de cobertura (usando uv)
	@echo "$(BLUE)Executando testes com cobertura (uv)...$(NC)"
	@uv run pytest --cov=src --cov-report=html --cov-report=term -s -v
	@echo "$(GREEN)✅ Testes concluídos!$(NC)"
	@echo "$(YELLOW)💡 Relatório HTML: htmlcov/index.html$(NC)"

.PHONY: test-cov-classic
test-cov-classic: ## Executa testes com relatório de cobertura (usando pip/venv tradicional)
	@echo "$(BLUE)Executando testes com cobertura (pip)...$(NC)"
	@pytest --cov=src --cov-report=html --cov-report=term -s -v
	@echo "$(GREEN)✅ Testes concluídos!$(NC)"
	@echo "$(YELLOW)💡 Relatório HTML: htmlcov/index.html$(NC)"

.PHONY: check
check: ## Roda todas as verificações (lint + test)
	@echo "$(BLUE)🔍 Executando todas as verificações...$(NC)"
	@echo ""
	@echo "$(YELLOW)1/2 Verificando código...$(NC)"
	@uv run ruff check . --no-fix
	@echo ""
	@echo "$(YELLOW)2/2 Executando testes...$(NC)"
	@uv run pytest -s -v
	@echo ""
	@echo "$(GREEN)✅ Todas as verificações passaram!$(NC)"

.PHONY: security
security: ## Verifica segurança do código e dependências
	@echo "$(BLUE)🛡️  Verificando segurança...$(NC)"
	@echo ""
	@echo "$(YELLOW)1/2 Analisando código com Bandit...$(NC)"
	@uv run bandit -r src/ || true
	@echo ""
	@echo "$(YELLOW)2/2 Verificando vulnerabilidades nas dependências...$(NC)"
	@uv run safety scan || echo "$(YELLOW)⚠️  Safety requer API key para verificação completa$(NC)"
	@echo ""
	@echo "$(GREEN)✅ Verificação de segurança concluída!$(NC)"

.PHONY: docker-build
docker-build: ## Constrói imagem Docker
	@echo "$(BLUE)🐳 Construindo imagem Docker...$(NC)"
	@docker build -t $(PROJECT_NAME):$(PROJECT_VERSION) .
	@docker tag $(PROJECT_NAME):$(PROJECT_VERSION) $(PROJECT_NAME):latest
	@echo "$(GREEN)✅ Imagem Docker construída!$(NC)"
	@echo "$(YELLOW)💡 Imagem: $(PROJECT_NAME):$(PROJECT_VERSION)$(NC)"

.PHONY: docker-run
docker-run: ## Inicia containers Docker
	@echo "$(BLUE)🐳 Iniciando containers Docker...$(NC)"
	@docker-compose up -d
	@echo "$(GREEN)✅ Containers iniciados!$(NC)"
	@echo "$(YELLOW)💡 Para ver logs: make docker-logs$(NC)"
	@echo "$(YELLOW)💡 Para parar: make docker-stop$(NC)"

.PHONY: docker-logs
docker-logs: ## Visualiza logs dos containers
	@echo "$(BLUE)🐳 Visualizando logs...$(NC)"
	@docker-compose logs -f

.PHONY: docker-stop
docker-stop: ## Para containers Docker
	@echo "$(YELLOW)🐳 Parando containers Docker...$(NC)"
	@docker-compose down
	@echo "$(GREEN)✅ Containers parados!$(NC)"

.PHONY: docker-clean
docker-clean: ## Remove containers e volumes Docker
	@echo "$(YELLOW)🐳 Limpando containers e volumes Docker...$(NC)"
	@docker-compose down -v
	@docker rmi $(PROJECT_NAME):$(PROJECT_VERSION) $(PROJECT_NAME):latest 2>/dev/null || true
	@echo "$(GREEN)✅ Limpeza Docker concluída!$(NC)"

.PHONY: clean
clean: ## Remove arquivos temporários e ambiente virtual
	@echo "$(YELLOW)Limpando arquivos temporários...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf htmlcov/ .coverage coverage.xml build/ dist/ 2>/dev/null || true
	@echo "$(BLUE)Removendo ambiente virtual...$(NC)"
	@rm -rf $(VENV_DIR) 2>/dev/null || true
	@echo "$(GREEN)✅ Limpeza concluída!$(NC)"

# Comando padrão
.DEFAULT_GOAL := help
