# PY-BLUEPRINT (MVC)

Um template simples para projetos Python estruturados em MVC (Model-View-Controller), com configurações para linting, testes e desenvolvimento.

## Estrutura do Projeto

```
src/
├── config/          # Configurações
├── controllers/     # Controladores
├── core/            # Lógica central
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

## Instalação

1. Clone o repositório:

   ```bash
   git clone <url-do-repo>
   cd py-blueprint
   ```

2. Instale as dependências:

   ```bash
   uv sync
   ```

   ```bash
   make install
   ```

## Desenvolvimento

- **Criar ambiente virtual**: `make venv`
- **Instalar dependências**: `make install`
- **Executar**: `make run`
- **Linting**: `make lint`
- **Formatar código**: `make format`
- **Testes**: `make test`
- **Limpar caches**: `make clean`

## Licença

MIT
