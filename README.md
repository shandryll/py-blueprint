# PY-BLUEPRINT (Hexagonal)

[![CI Pipeline](https://github.com/shandryll/py-blueprint/actions/workflows/checks.yml/badge.svg)](https://github.com/shandryll/py-blueprint/actions/workflows/checks.yml)
[![codecov](https://codecov.io/gh/shandryll/py-blueprint/branch/main/graph/badge.svg)](https://codecov.io/gh/shandryll/py-blueprint)

Template Python em **Arquitetura Hexagonal** (Ports & Adapters) com FastAPI: configuração de lint, testes e ambiente pronta para novos projetos.

---

## Estrutura do projeto

```
py-blueprint/
├── src/
│   ├── domain/                              # Núcleo do domínio (sem dependências externas)
│   │   ├── entities/                        # Entidades de domínio (dataclasses puras)
│   │   │   └── product.py                   # Product: regras de negócio, validação
│   │   ├── exceptions/                      # Exceções de domínio
│   │   │   └── product_exceptions.py        # ProductNotFoundError, ProductNameAlreadyExistsError, etc.
│   │   └── ports/                           # Interfaces (contratos)
│   │       ├── input/                       # Input Ports (casos de uso)
│   │       │   └── product_use_case.py      # IProductUseCase
│   │       └── output/                      # Output Ports (repositórios)
│   │           └── product_repository.py    # IProductRepository
│   ├── application/                         # Casos de uso (orquestração)
│   │   ├── use_cases/
│   │   │   └── product_use_case.py          # ProductUseCase (implementa IProductUseCase)
│   │   └── __init__.py
│   ├── infrastructure/                      # Adaptadores (frameworks, bibliotecas)
│   │   ├── di/                              # Injeção de dependência
│   │   │   └── container.py                 # get_product_use_case() — fábricas manuais
│   │   ├── input/                           # Adaptadores de entrada
│   │   │   └── http/
│   │   │       └── fastapi/
│   │   │           ├── main.py              # create_app() — FastAPI factory
│   │   │           ├── handlers.py          # Exception handlers (JSON padronizado)
│   │   │           ├── middleware.py        # HttpLoggingMiddleware (correlation ID)
│   │   │           ├── routes/
│   │   │           │   ├── health.py        # GET /api/v1/health
│   │   │           │   └── products.py      # CRUD /api/v1/products
│   │   │           └── schemas/
│   │   │               ├── product_schemas.py  # Pydantic schemas (entrada/saída HTTP)
│   │   │               └── health_schemas.py   # Health check schema
│   │   └── output/                          # Adaptadores de saída
│   │       └── persistence/
│   │           └── in_memory/
│   │               └── product_repository.py  # InMemoryProductRepository
│   ├── shared/                              # Código compartilhado (framework-agnostic)
│   │   ├── settings.py                      # Configurações (pydantic-settings + .env)
│   │   ├── exceptions.py                    # ApplicationServiceError
│   │   └── logger.py                        # Logger (structlog) com correlation ID
│   └── main.py                              # App FastAPI (entrada principal)
├── tests/
│   ├── conftest.py                          # Fixtures compartilhadas
│   ├── integration/                         # Testes contra a API (TestClient)
│   └── unit/                                # Testes por camada
│       ├── core/exceptions/                 # Testes de erro/handlers
│       ├── entities/                        # Testes das entidades de domínio
│       └── use_cases/                       # Testes dos casos de uso
├── docs/
│   ├── hexagonal-migration.md               # Guia da migração MVC → Hexagonal
│   └── guide-for-beginners.md               # Passo a passo para iniciantes
├── pyproject.toml                           # Dependências, pytest, ruff, pyright
└── Makefile                                 # Comandos: dev, lint, format, test, sync
```

**Fluxo de uma requisição:**
```
HTTP → Route → Schema (Pydantic) → IProductUseCase → ProductUseCase → IProductRepository → InMemoryProductRepository
       │                                                                                         │
       ← ProductResponseSchema ←─────────────────────────────────────────────────────────────────←
```

O **domínio** (`Product`, `IProductUseCase`, `IProductRepository`) não importa nada externo — nem FastAPI, nem Pydantic, nem banco de dados. Essa é a essência da arquitetura hexagonal: o núcleo de negócio é puro Python.

---

## Camadas (resumo)

| Camada | O que contém | Depende de |
|--------|-------------|------------|
| `domain/` | Entidades (dataclass), Exceções, Ports (interfaces) | Nada externo |
| `application/` | Casos de uso (orquestração) | `domain/` |
| `infrastructure/` | Adaptadores: FastAPI (input), repositórios (output), DI | `domain/`, `application/`, `shared/` |
| `shared/` | Config, logging, erros genéricos | Pydantic-settings, structlog |

---

## Versionamento da API

Todos os endpoints são versionados com prefixo `/api/v1/`:

- **Health Check**: `GET /api/v1/health`
- **Produtos**: `GET /api/v1/products/`, `POST /api/v1/products/`, `PUT /api/v1/products/{id}`, etc.

Isso permite evoluir a API sem quebrar clientes: no futuro, `/api/v2/` pode conviver com `/api/v1/`.

---

## Logging e Observabilidade

### Logging Estruturado (JSON)

Toda requisição HTTP é registrada automaticamente pelo middleware com:

- **Correlation ID** (`X-Correlation-ID`): rastreamento distribuído entre serviços
- **Método HTTP**: GET, POST, PUT, DELETE, etc.
- **Caminho**: `/api/v1/products`
- **Status code**: 200, 201, 404, 500, etc.
- **Duração**: tempo de processamento em ms
- **IP do cliente**: para auditoria

**Exemplo de log (JSON)**:

```json
{
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "event": "http_request",
  "method": "POST",
  "path": "/api/v1/products",
  "status_code": 201,
  "duration_ms": 2.45,
  "client_ip": "127.0.0.1",
  "level": "info",
  "timestamp": "2026-02-14T00:45:23.123456Z"
}
```

### Logs de Negócio

Operações criticamente importantes (criar, atualizar, deletar) também geram logs:

```json
{
  "event": "Product created",
  "operation": "create_product",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "level": "info",
  "timestamp": "2026-02-14T00:45:23.235456Z"
}
```

### Correlation ID em Arquitetura Distribuída

O Correlation ID pode ser passado entre serviços para rastreamento fim-a-fim:

```bash
curl -H "X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440000" \
  http://localhost:8000/api/v1/health
```

A resposta retorna o Correlation ID no header para confirmar:

```
X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440000
```

---

## Pré-requisitos

- **Python 3.12+**
- **uv** (recomendado) ou **pip** + **venv**

---

## Instalação

### Com uv (recomendado)

```bash
git clone <url-do-repo>
cd py-blueprint
uv venv
# Ativar: source .venv/bin/activate (Linux/Mac) ou .venv\Scripts\Activate.ps1 (Windows)
uv sync --dev
```

### Com pip

```bash
git clone <url-do-repo>
cd py-blueprint
python -m venv .venv
# Ativar o .venv
pip install -e ".[dev]"
```

_(Opcional)_ Hooks de pre-commit: `uv run pre-commit install`

**Arquivos de requirements (gerados)** — Gerados a partir do `pyproject.toml` (somente dependências diretas, fáceis de ler). Não edite manualmente. Para gerar/atualizar: `make requirements`.

| Arquivo                | Uso                                      | Conteúdo                                   |
| ---------------------- | ---------------------------------------- | ------------------------------------------ |
| `requirements.txt`     | Produção / deploy                        | Apenas dependências de runtime             |
| `requirements-dev.txt` | Desenvolvimento sem uv (pip, IDEs, etc.) | Runtime + dev (pytest, ruff, bandit, etc.) |

Gerados pelo script `scripts/export_requirements.py` (lê apenas o que está declarado no `pyproject.toml`).

---

## Desenvolvimento

| Ação                            | Make                | UV                                                                | Pip / Python (venv ativo)                                          |
| ------------------------------- | ------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------ |
| Gerar requirements (prod + dev) | `make requirements` | —                                                                 | `python scripts/export_requirements.py`                            |
| Sincronizar deps                | `make sync`         | `uv sync --dev`                                                   | `pip install -e ".[dev]"` ou `pip install -r requirements-dev.txt` |
| Subir a API                     | `make dev`          | `uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload` | `uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload`         |
| Lint + correção                 | `make lint`         | `uv run ruff check . --fix`                                       | `ruff check . --fix`                                               |
| Formatar                        | `make format`       | `uv run ruff format .`                                            | `ruff format .`                                                    |
| Testes                          | `make test`         | `uv run pytest -v`                                                | `pytest -v`                                                        |
| Testes + cobertura              | —                   | `uv run pytest --cov=src --cov-report=term -v`                    | `pytest --cov=src --cov-report=term -v`                            |

A API sobe em **http://0.0.0.0:8000**. Documentação interativa: **http://localhost:8000/docs**.

---

## Configuração

Crie um `.env` na raiz (opcional; há valores padrão):

```env
APP_NAME=Py-Blueprint
APP_VERSION=1.0.0
DEBUG=false
HOST=127.0.0.1
PORT=8000
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
LOG_LEVEL=INFO
LOG_FORMAT_JSON=false
```

- **LOG_FORMAT_JSON**: `false` = logs em texto (dev), `true` = JSON (produção/observabilidade).
- **DEBUG**: quando `true`, é repassado ao FastAPI e o **nível de log** passa a ser DEBUG automaticamente (logs de debug aparecem no terminal). Quando `false`, o nível de log segue **LOG_LEVEL**.

---

## Docker

```bash
docker build -t py-blueprint .
docker compose up -d
```

---

## O que este template oferece

- **API Versionada**: endpoints estruturados com `/api/v1/` para evolução sem quebrar clientes.
- **Arquitetura Hexagonal** (Ports & Adapters):
  - Domínio puro (dataclasses, sem Pydantic, sem FastAPI)
  - Input/Output Ports bem definidos
  - Casos de uso orquestrando o fluxo
  - Adaptadores de entrada (FastAPI) e saída (repositórios) intercambiáveis
- **Configuração centralizada** com `pydantic-settings` e `.env`.
- **Erros padronizados**: `ApplicationServiceError` + `ProductDomainError` + handlers FastAPI (resposta JSON com timestamp e path).
- **Logging estruturado** (structlog):
  - JSON para observabilidade (produção)
  - Texto formatado para desenvolvimento
  - **Correlation ID automático** para rastreamento distribuído
  - Middleware HTTP que loga todas as requisições com duração e status code
- **Injeção de dependência** manual via `infrastructure/di/container.py` (sem framework de DI externo).
- **Interface de repositório** (`IProductRepository`) e implementação em memória (troque por SQL/Redis sem tocar no domínio).
- **Testes**: unitários (use case isolado) e integração (API real com `TestClient`); pytest configurado em `pyproject.toml`.
- **Qualidade**: Ruff (lint/format), Pyright, Bandit, Safety; CI com GitHub Actions.

---

## Estrutura de código (resumo)

- **`domain/entities/product.py`**: Entidade `Product` como dataclass pura — valida nome, preço e estoque na criação; método `update()` imutável (retorna nova instância).
- **`domain/ports/`**: Contratos `IProductUseCase` (input) e `IProductRepository` (output). O domínio só conhece interfaces.
- **`application/use_cases/product_use_case.py`**: `ProductUseCase` implementa `IProductUseCase` e orquestra regras (verificar duplicidade, salvar, buscar).
- **`infrastructure/input/http/fastapi/`**: Adaptador de entrada — rotas FastAPI que convertem schemas Pydantic em chamadas ao caso de uso.
- **`infrastructure/output/persistence/in_memory/`**: Adaptador de saída — repositório em memória (troque por SQLAlchemy/asyncpg sem alterar o domínio).
- **`infrastructure/di/container.py`**: `get_product_use_case()` — injeta o caso de uso lendo `app.state`, sem singleton global ou framework de DI.
- **`infrastructure/input/http/fastapi/handlers.py`**: Handlers FastAPI para `ApplicationServiceError`, `ProductDomainError`, HTTPException e `RequestValidationError`.
- **`infrastructure/input/http/fastapi/middleware.py`**: `HttpLoggingMiddleware` — correlation ID, método, path, status, duração.
- **`shared/settings.py`**: `get_settings()` retorna configurações com cache (singleton).
- **`shared/logger.py`**: `get_logger(__name__)` para logs estruturados com correlation ID.
- **`shared/exceptions.py`**: `ApplicationServiceError` com `message`, `error_code`, `status_code`.

---

## CI/CD

- **checks.yml** (CI Pipeline): execução em sequência — lint (Ruff) → testes com cobertura (Codecov) → security (Bandit, Safety). Dispara em pushes/PRs para `main` e agendado nos dias 1 e 16 de cada mês.

---

## Troubleshooting

- **Python não encontrado (Windows)**: instale em [python.org](https://www.python.org/downloads/) e marque "Add Python to PATH"; ou use `py -m venv .venv`.
- **Erros de TLS com uv**: tente `UV_NATIVE_TLS=false uv sync --dev` ou use `pip install -e ".[dev]"`.
- **Logs aparecendo nos testes**: use `make test` (sem `-s`); o pytest captura stdout/stderr. Se usar `pytest -s`, os logs voltam a aparecer.
- **Dois logs para a mesma requisição**: é normal. Um vem da operação de negócio (ex.: "Product created") e outro do middleware HTTP ("http_request"). Os timestamps mostram a sequência verdadeira.

---

## Contribuição

Veja [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença

MIT
