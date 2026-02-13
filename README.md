# PY-BLUEPRINT (MVC)

[![Linter and Formatter Checks](https://github.com/shandryll/py-blueprint/actions/workflows/checks.yml/badge.svg)](https://github.com/shandryll/py-blueprint/actions/workflows/checks.yml)
[![Security Checks](https://github.com/shandryll/py-blueprint/actions/workflows/security.yml/badge.svg)](https://github.com/shandryll/py-blueprint/actions/workflows/security.yml)

Um template simples para projetos Python estruturados em MVC (Model-View-Controller), com configurações para linting, testes e desenvolvimento.

## Estrutura do Projeto

```
src/
├── core/            # Lógica central
│   ├── config/      # Configurações (pydantic-settings)
│   └── exceptions/  # Exceções customizadas e handlers HTTP
├── controllers/     # Controllers (MVC) - Coordenam lógica entre routes e services
│   └── factories/   # Factories para criação de controllers (injeção de dependências)
├── models/          # Modelos de dados (MVC) - Pydantic models
├── repositories/    # Repositórios de dados - Acesso aos dados
│   └── interfaces/  # Interfaces para repositórios (BaseRepository)
├── routes/          # Definições de rotas HTTP (MVC) - Endpoints da API
│   ├── examples/    # Rotas de examples (organizadas por verbo HTTP)
│   │   ├── get.py   # Rotas GET
│   │   ├── post.py  # Rotas POST
│   │   ├── put.py   # Rotas PUT
│   │   └── delete.py# Rotas DELETE
│   └── health/      # Rotas de health check
├── services/        # Serviços de negócio - Lógica de negócio
│   └── factories/   # Factories para criação de serviços (injeção de dependências)
├── utils/           # Utilitários (ex: configuração de logging)
└── views/           # Views para formatação de respostas (MVC)
tests/               # Testes (estrutura espelha src/)
├── unit/            # Testes unitários
│   ├── core/        # Testes do módulo core
│   ├── repositories/# Testes de repositórios
│   ├── services/    # Testes de serviços
│   ├── routes/      # Testes de rotas
│   └── test_main.py # Testes do módulo main
├── integration/     # Testes de integração
│   └── routes/      # Testes de integração de rotas
└── e2e/             # Testes end-to-end
requirements/        # Arquivos de dependências para pip
├── base.txt         # Dependências de runtime (produção)
└── dev.txt          # Dependências de desenvolvimento (inclui base.txt)
```

## Pré-requisitos

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recomendado) ou pip (alternativa)
- Make (no Windows, instale via [Chocolatey](https://chocolatey.org/): `choco install make`)
- [pre-commit](https://pre-commit.com/) (opcional, para hooks locais)

## Instalação

### Opção 1: Usando UV (Recomendado)

1. Clone o repositório:

   ```bash
   git clone <url-do-repo>
   cd py-blueprint
   ```

2. Setup completo:

   ```bash
   make setup
   ```

   Ou passo a passo:

   ```bash
   make venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate     # Windows
   make install
   ```

### Opção 2: Usando PIP/Venv Tradicional (Alternativa)

Se você tiver problemas com TLS ao usar `uv` ou preferir o método tradicional, pode usar `pip` com `venv`:

1. Clone o repositório:

   ```bash
   git clone <url-do-repo>
   cd py-blueprint
   ```

2. Setup completo:

   ```bash
   make setup-classic
   ```

   Ou passo a passo:

   ```bash
   make venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate     # Windows
   make install-classic
   ```

   **Nota sobre dependências**: Os arquivos de requirements estão organizados em `requirements/`:
   - `requirements/base.txt`: Apenas dependências de runtime (produção)
   - `requirements/dev.txt`: Dependências de desenvolvimento (inclui base.txt + ferramentas)

   Para instalação manual:

   ```bash
   # Apenas runtime
   pip install -r requirements/base.txt

   # Desenvolvimento completo
   pip install -r requirements/dev.txt
   ```

## Desenvolvimento

### Comandos com UV (Padrão)

- **Setup completo**: `make setup`
- **Criar ambiente virtual**: `make venv`
- **Instalar dependências**: `make install`
- **Executar aplicação**: `make run`
- **Linting**: `make lint`
- **Formatar código**: `make format`
- **Testes**: `make test`
- **Testes com cobertura**: `make test-cov`
- **Verificar tudo**: `make check` (lint + test)
- **Verificar segurança**: `make security`
- **Limpar caches**: `make clean`
- **Instalar hooks de pre-commit**: `make pre-commit-install` (opcional, roda checagens antes de commits)

## Configuração

O projeto usa `pydantic-settings` para gerenciar configurações. Crie um arquivo `.env` na raiz do projeto baseado nas variáveis abaixo:

```env
# Aplicação
APP_NAME=Py-Blueprint
APP_VERSION=0.1.0
DEBUG=false

# Servidor
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=["http://localhost:3000"]
LOG_LEVEL=INFO
```

## Docker

O projeto inclui suporte para Docker:

```bash
# Build da imagem
docker build -t py-blueprint .

# Executar com Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## Funcionalidades

- ✅ Estrutura MVC completa
- ✅ Configuração centralizada com pydantic-settings
- ✅ Tratamento de erros global (exception handlers)
- ✅ Middleware de logging
- ✅ CORS configurável
- ✅ Versionamento dinâmico do pyproject.toml
- ✅ Docker e Docker Compose
- ✅ CI/CD com GitHub Actions
- ✅ Testes com pytest e cobertura
- ✅ Linting e formatação com Ruff
- ✅ Segurança com Bandit e Safety

## CI/CD Pipeline

Este template inclui uma esteira de Integração Contínua (CI) e Implantação Contínua (CD) automatizada usando GitHub Actions. Ela roda automaticamente em pushes e pull requests na branch `main`, garantindo qualidade e segurança do código. Aqui vai uma explicação simples do que cada parte faz:

### Workflows Automatizados

- **Checks (checks.yml)**: Executa verificações rápidas em cada mudança de código.
  - **Job Linting**: Verifica estilo, formatação e dependências atualizadas (usando Ruff e uv).
  - **Job Testes**: Roda os testes unitários, mede a cobertura e envia relatório para Codecov.
- **Security (security.yml)**: Focado em segurança, roda em pushes/PRs e semanalmente (segunda-feira).
  - **Job Segurança**: Analisa código e pacotes para vulnerabilidades e versões desatualizadas (usando Bandit, Safety e pip).

Para ver os resultados, acesse a aba "Actions" no GitHub após um push ou PR.

## Estrutura de Código

### Exemplo de Repository Interface

Veja `src/repositories/interfaces/base_repository.py` para a interface base que todos os repositórios devem implementar.

## Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes de contribuição.

### Comandos com PIP/Venv Tradicional (Alternativa)

- **Setup completo**: `make setup-classic`
- **Instalar dependências**: `make install-classic`
- **Executar aplicação**: `make run-classic`
- **Linting**: `make lint-classic`
- **Formatar código**: `make format-classic`
- **Testes**: `make test-classic`
- **Testes com cobertura**: `make test-cov-classic`

### Comandos Adicionais

- **Instalar hooks de pre-commit**: `make pre-commit-install` (opcional)
- **Ver ajuda completa**: `make help`

## Configuração

O projeto usa `pydantic-settings` para gerenciar configurações. Crie um arquivo `.env` na raiz do projeto baseado nas variáveis abaixo:

```env
# Aplicação
APP_NAME=Py-Blueprint
APP_VERSION=0.1.0
DEBUG=false

# Servidor
HOST=0.0.0.0
PORT=8000

# CORS (obrigatório configurar em produção)
CORS_ORIGINS=["http://localhost:3000"]

# Logging
LOG_LEVEL=INFO
LOG_FORMAT_JSON=false  # true para formato JSON (produção), false para texto (desenvolvimento)
```

## Docker

O projeto inclui suporte para Docker:

```bash
# Build da imagem
docker build -t py-blueprint .

# Executar com Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## Funcionalidades

- ✅ **Estrutura MVC completa** - Model, View, Controller bem definidos
- ✅ **Rotas organizadas por verbos HTTP** - Estrutura em pastas separadas (GET, POST, PUT, DELETE)
- ✅ **Configuração centralizada** - pydantic-settings com suporte a `.env`
- ✅ **Tratamento de erros global** - Exception handlers HTTP padronizados
- ✅ **Logging estruturado com structlog** - Logs estruturados com suporte a JSON e texto, pronto para observabilidade
- ✅ **Exception handlers padronizados** - ApplicationServiceError com handlers FastAPI
- ✅ **CORS configurável** - Valores padrão seguros, fácil configuração
- ✅ **Interface base para repositórios** - BaseRepository com type parameters (Python 3.12)
- ✅ **Factory Pattern** - Injeção de dependências para controllers e services
- ✅ **Type hints modernos** - Python 3.12 com sintaxe atualizada
- ✅ **Docker e Docker Compose** - Pronto para containerização
- ✅ **CI/CD com GitHub Actions** - Pipeline automatizado de qualidade
- ✅ **Testes completos** - pytest com cobertura de código
- ✅ **Linting e formatação** - Ruff configurado e pronto
- ✅ **Segurança** - Bandit e Safety integrados
- ✅ **Suporte a UV e PIP** - Duas formas de instalar e executar o projeto

## CI/CD Pipeline

Este template inclui uma esteira de Integração Contínua (CI) e Implantação Contínua (CD) automatizada usando GitHub Actions. Ela roda automaticamente em pushes e pull requests na branch `main`, garantindo qualidade e segurança do código. Aqui vai uma explicação simples do que cada parte faz:

### Workflows Automatizados

- **Checks (checks.yml)**: Executa verificações rápidas em cada mudança de código.
  - **Job Linting**: Verifica estilo, formatação e dependências atualizadas (usando Ruff e uv).
  - **Job Testes**: Roda os testes unitários, mede a cobertura e envia relatório para Codecov.
- **Security (security.yml)**: Focado em segurança, roda em pushes/PRs e semanalmente (segunda-feira).
  - **Job Segurança**: Analisa código e pacotes para vulnerabilidades e versões desatualizadas (usando Bandit, Safety e pip).

Para ver os resultados, acesse a aba "Actions" no GitHub após um push ou PR.

## Estrutura de Código

### Módulo Core (`src/core/`)

O módulo `core` contém a lógica fundamental da aplicação. Aqui está o que cada arquivo faz:

#### 📋 `config/` - Configurações da Aplicação

**Arquivo principal:** `config/settings.py`

**O que faz:** Gerencia todas as configurações da aplicação de forma centralizada.

**Por que é importante:**

- Evita ter configurações espalhadas pelo código
- Permite alterar configurações sem mexer no código (via arquivo `.env` ou variáveis de ambiente)
- Valida automaticamente se as configurações estão corretas

**Exemplo de uso:**

```python
from src.core.config.settings import get_settings

settings = get_settings()
print(settings.app_name)  # "Py-Blueprint"
print(settings.port)       # 8000
```

**Principais configurações:**

- `app_name`, `app_version`: Informações da aplicação
- `host`, `port`: Onde o servidor vai rodar
- `cors_origins`: Quais sites podem fazer requisições para sua API
- `log_level`: Nível de detalhamento dos logs (DEBUG, INFO, WARNING, ERROR)
- `log_format_json`: Formato dos logs (true = JSON para produção, false = texto para desenvolvimento)

---

#### ⚠️ `exceptions/` - Exceções e Handlers

**Arquivos principais:**

- `errors.py`: Exceções customizadas (ApplicationServiceError) e constantes HTTP
- `fastapi_handlers.py`: Handler específico do FastAPI para ApplicationServiceError

**O que faz:** Define tipos de erros personalizados para sua aplicação e como tratá-los.

**Por que é importante:**

- Permite criar erros específicos para sua aplicação
- Facilita identificar onde ocorreu o erro (qual serviço falhou)
- Padroniza como os erros são tratados

**Exemplo de uso:**

```python
from src.core.exceptions import ApplicationServiceError, HTTP_404_NOT_FOUND

# Erro de negócio (cliente) - retorna 404
raise ApplicationServiceError(
    service_name="ExampleService",
    message="Example não encontrado",
    status_code=HTTP_404_NOT_FOUND,
    error_code="EXAMPLE_NOT_FOUND"
)

# Erro interno (servidor) - retorna 500
raise ApplicationServiceError(
    service_name="DatabaseService",
    message="Conexão com banco falhou",
    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    error_code="DATABASE_CONNECTION_ERROR"
)
```

**Tratamento manual de erros em services:**

```python
from src.utils.logging import get_logger

logger = get_logger(__name__)

try:
    # Sua lógica aqui
    result = await repository.get_by_id(id)
except ApplicationServiceError:
    # Re-lança ApplicationServiceError sem modificar
    raise
except Exception as err:
    # Converte outras exceções para ApplicationServiceError
    logger.error("Erro ao buscar", operation="get_by_id", error_code="GET_ERROR")
    raise ApplicationServiceError(
        service_name="ExampleService",
        message=f"Erro ao buscar: {str(err)}",
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="GET_ERROR",
    ) from err
```

**Exemplo com decorator (recomendado):**

```python
from src.core.exceptions import handle_service_errors_async
from src.utils.logging import get_logger

logger = get_logger(__name__)

class ProductService:
    SERVICE_NAME = "ProductService"

    @handle_service_errors_async(
        service_name=SERVICE_NAME,
        error_code="CREATE_ERROR",
    )
    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        logger.debug("Criando produto", operation="create_product")
        # Sua lógica aqui
        # Se ocorrer erro, o decorator loga automaticamente e converte para ApplicationServiceError
        return product
```

O decorator automaticamente:

- Loga todos os erros com contexto estruturado (operation, function, service, error_type, error_code)
- Converte exceções não tratadas para ApplicationServiceError
- Mantém o rastreamento de erros para observabilidade

**Quando usar:** Sempre que você criar um serviço (em `src/services/`) e precisar lançar um erro específico.

**Nota:** Use o decorator `@handle_service_errors_async` nos métodos dos serviços para tratamento automático de erros. Ele loga todos os erros de forma estruturada para observabilidade.

---

#### 🛡️ `exceptions/fastapi_handlers.py` - Tratamento Global de Erros

**Localização:** `exceptions/fastapi_handlers.py`

**O que faz:** Define como a aplicação responde quando ocorrem erros `ApplicationServiceError`.

**Por que é importante:**

- Garante que todos os erros retornem respostas padronizadas em JSON
- Adiciona informações úteis como timestamp e path da requisição
- Melhora a experiência de quem usa sua API (respostas consistentes)

**Como usar:**
No `main.py`, registre o handler:

```python
from fastapi import FastAPI
from src.core.exceptions.application_errors import ApplicationServiceError
from src.core.exceptions.fastapi_handlers import application_error_handler

app = FastAPI()
app.add_exception_handler(ApplicationServiceError, application_error_handler)
```

**Exemplo de resposta de erro:**

```json
{
  "service": "ExampleService",
  "message": "Example não encontrado",
  "error_code": "EXAMPLE_NOT_FOUND",
  "status_code": 404,
  "timestamp": "2024-01-15T10:30:00+00:00",
  "path": "/api/examples/123"
}
```

**Campos da resposta padronizada:**

- `service`: Nome do serviço que gerou o erro (ex: "ExampleService")
- `message`: Mensagem descritiva do erro
- `error_code`: Código de erro específico para tratamento programático (ex: "EXAMPLE_NOT_FOUND")
- `status_code`: Código HTTP de status (ex: 404, 500)
- `timestamp`: Quando o erro ocorreu (formato ISO 8601)
- `path`: Caminho da requisição que causou o erro

---

#### 🔧 `utils/` - Utilitários

**Arquivo principal:** `utils/logging.py`

**O que faz:** Fornece logging estruturado usando `structlog` com suporte a formato JSON e texto.

**Por que é importante:**

- Logs estruturados prontos para ferramentas de observabilidade (Datadog, ELK, CloudWatch)
- Suporte a formato JSON (produção) e texto (desenvolvimento)
- Configuração automática e simples
- Contexto estruturado para facilitar queries e análise

**Exemplo de uso:**

```python
from src.utils.logging import get_logger

# Criar logger para o módulo
logger = get_logger(__name__)

# Log simples
logger.info("Operação concluída")

# Log com contexto estruturado
logger.info("Produto criado", operation="create_product")
logger.error("Erro ao processar", operation="process_data", error_code="PROCESS_ERROR")
```

**Formato de saída:**

**Texto (desenvolvimento - `LOG_FORMAT_JSON=false`):**

```
2026-02-12T19:24:43.534471Z [info     ] Produto criado                    operation=create_product
```

**JSON (produção - `LOG_FORMAT_JSON=true`):**

```json
{
  "event": "Produto criado",
  "level": "info",
  "operation": "create_product",
  "timestamp": "2026-02-12T19:24:43.534471Z"
}
```

**Configuração:**
Configure no arquivo `.env`:

```env
LOG_LEVEL=INFO
LOG_FORMAT_JSON=false  # false = texto, true = JSON
```

**Como funciona:**

- `get_logger(__name__)`: Obtém um logger configurado para o módulo
- Configuração automática: O logging é configurado automaticamente na primeira chamada usando structlog
- Suporte a observabilidade: Logs estruturados facilitam integração com ferramentas de monitoramento

---

### Arquitetura MVC

O projeto segue o padrão **Model-View-Controller (MVC)**:

#### 📋 Model (`models/`)

- Define a estrutura de dados usando Pydantic
- Validação automática de dados de entrada/saída
- Exemplo: `ExampleCreate`, `ExampleUpdate`, `ExampleResponse`

#### 🎮 Controller (`controllers/`)

- Coordena a lógica entre routes e services
- Não contém lógica de negócio, apenas orquestra chamadas
- Exemplo: `ExampleController`, `HealthController`

#### 👁️ View (`views/`)

- Formatação de respostas (geralmente via Pydantic `response_model`)
- Pode ser usado para transformações adicionais quando necessário

#### 🔄 Fluxo MVC Completo

```
HTTP Request
    ↓
Routes (define endpoints)
    ↓
Controllers (coordena)
    ↓
Services (lógica de negócio)
    ↓
Repositories (acesso aos dados)
    ↓
Models (estrutura de dados)
    ↓
Views (formatação de resposta)
    ↓
HTTP Response
```

---

### Resumo Visual do Fluxo

```
1. Requisição chega → routes → controllers → services → repositories
2. Se der erro → exceptions/fastapi_handlers.py (formata o erro)
3. Resposta é enviada → HTTP Response
```

### Exemplo de Repository Interface

Veja `src/repositories/interfaces/base_repository.py` para a interface base que todos os repositórios devem implementar. A interface usa type parameters do Python 3.12 (`BaseRepository[T, ID]`).

## Troubleshooting

### Problemas com Certificado SSL/TLS

Se você encontrar erros relacionados a TLS ao usar `uv`, você tem duas opções:

#### Opção 1: Usar PIP (Recomendado para problemas de TLS)

Use os comandos alternativos com `pip`:

```bash
make setup-classic
make run-classic
```

#### Opção 2: Configurar UV para resolver TLS

**Solução 1: Usar certificados do sistema**

```bash
export UV_NATIVE_TLS=false
make install
```

**Solução 2: Configurar certificado SSL personalizado**

```bash
export SSL_CERT_FILE=/caminho/para/seu/certificado.pem
# ou
export REQUESTS_CA_BUNDLE=/caminho/para/seu/certificado.pem
```

**Solução 3: Verificar proxy corporativo**

```bash
export HTTP_PROXY=http://proxy.empresa.com:8080
export HTTPS_PROXY=http://proxy.empresa.com:8080
export NO_PROXY=localhost,127.0.0.1
```

**Solução 4: Atualizar certificados (macOS)**

```bash
brew install ca-certificates
```

### Estrutura de Rotas

As rotas estão organizadas em pastas por recurso, e dentro de cada pasta, separadas por verbos HTTP:

```
src/routes/
├── examples/
│   ├── __init__.py    # Combina todos os routers
│   ├── get.py         # GET /api/examples/ e GET /api/examples/{id}
│   ├── post.py        # POST /api/examples/
│   ├── put.py         # PUT /api/examples/{id}
│   └── delete.py      # DELETE /api/examples/{id}
└── health/
    ├── __init__.py    # Combina todos os routers
    └── get.py         # GET /health/
```

Esta estrutura facilita a organização e manutenção quando o projeto cresce.

## Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes de contribuição.

## Licença

MIT
