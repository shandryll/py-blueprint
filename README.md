# PY-BLUEPRINT (MVC)

[![CI Pipeline](https://github.com/shandryll/py-blueprint/actions/workflows/checks.yml/badge.svg)](https://github.com/shandryll/py-blueprint/actions/workflows/checks.yml)
[![codecov](https://codecov.io/gh/shandryll/py-blueprint/branch/main/graph/badge.svg)](https://codecov.io/gh/shandryll/py-blueprint)

Template Python em **MVC** (Model-Controller) com FastAPI: configuração de lint, testes e ambiente pronta para novos projetos.

---

## Estrutura do projeto

```
py-blueprint/
├── src/
│   ├── core/                           # Núcleo da aplicação
│   │   ├── settings/                   # Configurações (pydantic-settings + .env)
│   │   └── exceptions/                 # Erros da aplicação e handlers HTTP
│   │       ├── application_errors.py   # ApplicationServiceError e códigos HTTP
│   │       ├── error_decorators.py     # Decorators para tratar erros em services
│   │       └── fastapi_handlers.py     # Handlers FastAPI (resposta JSON padronizada)
│   ├── controllers/                    # MVC: coordenam rotas e serviços
│   ├── factories/                      # Criação de repositório, service e controller (injeção de dependência)
│   ├── models/                         # MVC: modelos Pydantic (entrada/saída)
│   ├── repositories/                   # Acesso a dados
│   │   ├── interfaces/                 # Contratos (ex.: IProductRepository)
│   │   └── in_memory/                  # Implementação em memória (ex.: produtos)
│   ├── routes/                         # Endpoints por recurso
│   │   ├── health/                     # GET /health/
│   │   └── products/                   # CRUD em /api/products/ (get, post, put, patch, delete)
│   ├── services/                       # Lógica de negócio
│   ├── utils/                          # Logger (structlog) e outros utilitários
│   └── main.py                         # App FastAPI, CORS, exception handlers, rotas
├── tests/
│   ├── conftest.py                     # Fixtures compartilhadas (client, product_service, etc.)
│   ├── integration/                    # Testes contra a API (TestClient)
│   └── unit/                           # Testes por camada (espelha src/)
│       ├── controllers/
│       ├── core/exceptions/
│       ├── models/
│       ├── repositories/in_memory/
│       └── services/
├── pyproject.toml                      # Dependências, pytest, ruff, pyright
└── Makefile                            # Comandos: dev, lint, format, test, sync
```

**Fluxo de uma requisição:** `Route` → `Controller` → `Service` → `Repository` → `Model`. Erros são tratados pelos **exception handlers** e devolvidos em JSON.

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

| Ação                            | Make                 | UV                                                    | Pip / Python (venv ativo) |
| ------------------------------- | -------------------- | ----------------------------------------------------- | ------------------------- |
| Gerar requirements (prod + dev) | `make requirements`  | —                                                     | `python scripts/export_requirements.py` |
| Sincronizar deps                | `make sync`          | `uv sync --dev`                                       | `pip install -e ".[dev]"` ou `pip install -r requirements-dev.txt` |
| Subir a API                     | `make dev`           | `uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload` | `uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload` |
| Lint + correção                 | `make lint`          | `uv run ruff check . --fix`                            | `ruff check . --fix`      |
| Formatar                        | `make format`        | `uv run ruff format .`                                 | `ruff format .`           |
| Testes                          | `make test`          | `uv run pytest -v`                                     | `pytest -v`                |
| Testes + cobertura              | —                    | `uv run pytest --cov=src --cov-report=term -v`         | `pytest --cov=src --cov-report=term -v` |

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
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000/"]
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

- **Model-Controller** com rotas por recurso e por verbo HTTP (get/post/put/patch/delete).
- **Configuração centralizada** com `pydantic-settings` e `.env`.
- **Erros padronizados**: `ApplicationServiceError` + decorators em services + handlers FastAPI (resposta JSON).
- **Logging estruturado** (structlog): texto ou JSON conforme `LOG_FORMAT_JSON`.
- **Injeção de dependência** via **factories** em `src/factories/` (repositório → service → controller).
- **Interface de repositório** (`IProductRepository`) e implementação em memória.
- **Testes**: unitários por camada e integração com `TestClient`; pytest configurado em `pyproject.toml` (sem `-s` para saída limpa).
- **Qualidade**: Ruff (lint/format), Pyright, Bandit, Safety; CI com GitHub Actions.

---

## Estrutura de código (resumo)

- **`core/settings`**: `get_settings()` retorna configurações (singleton). Use em toda a app.
- **`core/exceptions`**:
  - `ApplicationServiceError`: erro de negócio com `message`, `error_code`, `status_code`.
  - `@handle_service_errors_async` / `@handle_service_errors_sync`: aplicados nos services para logar e converter exceções.
  - Handlers em `fastapi_handlers` transformam esses erros em resposta JSON (timestamp, path, etc.).
- **`factories`**: `make_product_repository()`, `make_product_service()`, `make_product_controller()` — usados nas rotas para injetar dependências.
- **`models`**: Pydantic (ex.: `ProductCreate`, `ProductUpdate`, `ProductResponse`).
- **`repositories`**: Interface em `interfaces/`, implementação em `in_memory/`.
- **`routes`**: Cada recurso tem uma pasta (ex.: `products/`) com arquivos por verbo (`get.py`, `post.py`, …); o `__init__.py` monta o router com prefixo e tags.
- **`utils/logger`**: `get_logger(__name__)` para logs estruturados (info/error com kwargs).

---

## CI/CD

- **checks.yml** (CI Pipeline): execução em sequência — lint (Ruff) → testes com cobertura (Codecov) → security (Bandit, Safety). Dispara em pushes/PRs para `main` e agendado nos dias 1 e 16 de cada mês.

---

## Troubleshooting

- **Python não encontrado (Windows)**: instale em [python.org](https://www.python.org/downloads/) e marque "Add Python to PATH"; ou use `py -m venv .venv`.
- **Erros de TLS com uv**: tente `UV_NATIVE_TLS=false uv sync --dev` ou use `pip install -e ".[dev]"`.
- **Logs aparecendo nos testes**: use `make test` (sem `-s`); o pytest captura stdout/stderr. Se usar `pytest -s`, os logs voltam a aparecer.

---

## Contribuição

Veja [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença

MIT
