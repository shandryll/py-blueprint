# PY-BLUEPRINT (MVC)

[![Linter and Formatter Checks](https://github.com/shandryll/py-blueprint/actions/workflows/checks.yml/badge.svg)](https://github.com/shandryll/py-blueprint/actions/workflows/checks.yml)
[![Security Checks](https://github.com/shandryll/py-blueprint/actions/workflows/security.yml/badge.svg)](https://github.com/shandryll/py-blueprint/actions/workflows/security.yml)

Um template simples para projetos Python estruturados em MVC (Model-View-Controller), com configurações para linting, testes e desenvolvimento.

## Estrutura do Projeto

```
src/
├── core/            # Lógica central (config, exceptions, decorators)
├── controllers/     # Controladores
├── models/          # Modelos de dados
├── repositories/    # Repositórios de dados
│   └── interfaces/  # Interfaces para repositórios
├── routes/          # Definições de rotas
├── services/        # Serviços de negócio
├── utils/           # Utilitários
└── views/           # Visualizações
tests/               # Testes
```

## Pré-requisitos

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recomendado para gerenciamento de dependências)
- Make (no Windows, instale via [Chocolatey](https://chocolatey.org/): `choco install make`)
- [pre-commit](https://pre-commit.com/) (opcional, para hooks locais: `pip install pre-commit`)

## Instalação

1. Clone o repositório:

   ```bash
   git clone <url-do-repo>
   cd py-blueprint
   ```

2. Instale as dependências:

   Para desenvolvimento (inclui ferramentas de dev):

   ```bash
   make install-dev
   ```

   Para produção (apenas dependências de runtime):

   ```bash
   make install-prod
   ```

## Desenvolvimento

- **Criar ambiente virtual**: `make venv`
- **Instalar dependências (dev)**: `make install-dev`
- **Instalar dependências (prod)**: `make install-prod`
- **Executar**: `make run`
- **Linting**: `make lint`
- **Formatar código**: `make format`
- **Testes**: `make test`
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

## Licença

MIT
