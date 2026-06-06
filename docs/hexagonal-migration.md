# Migração MVC → Arquitetura Hexagonal

## O que é Arquitetura Hexagonal?

A Arquitetura Hexagonal (também chamada de **Ports & Adapters**) é um padrão de projeto que organiza o código em **camadas concêntricas**:

```
┌─────────────────────────────────────┐
│         INFRASTRUCTURE              │
│  ┌───────────────────────────────┐  │
│  │       APPLICATION             │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │        DOMAIN           │  │  │
│  │  │  (Regras de Negócio)    │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

- **Domínio (Domain)**: O coração do sistema. Contém apenas regras de negócio, **sem dependências externas** (sem FastAPI, sem banco de dados, sem frameworks).
- **Aplicação (Application)**: Orquestra os casos de uso. Conecta o domínio com o mundo externo através de **Ports** (interfaces).
- **Infraestrutura (Infrastructure)**: Implementações concretas dos adapters (HTTP, banco de dados, APIs externas).
- **Compartilhado (Shared)**: Código transversal usado por todas as camadas (logger, configurações, exceções base).

---

## Antes (MVC)

```
src/
├── controllers/        # Controladores (HTTP)
│   ├── product_controller.py
│   └── health_controller.py
├── services/           # Lógica de negócio
│   └── product_service.py
├── models/             # Modelos Pydantic
│   └── product.py
├── repositories/       # Acesso a dados
│   ├── interfaces/
│   │   └── product_repository.py
│   └── in_memory/
│       └── in_memory_product_repository.py
├── routes/             # Rotas FastAPI
│   ├── products/
│   │   ├── __init__.py
│   │   ├── get.py
│   │   ├── post.py
│   │   ├── put.py
│   │   ├── patch.py
│   │   └── delete.py
│   └── health/
│       └── get.py
├── factories/          # Fábricas de dependências
│   └── product_factory.py
├── core/               # Config, exceções, middleware
│   ├── settings/
│   ├── exceptions/
│   └── middleware/
├── utils/              # Logger
│   └── logger.py
└── main.py
```

### Problemas do MVC:
- **Controllers e Services com responsabilidades misturadas**
- **Modelos Pydantic usados tanto para domínio quanto para API** (acoplamento)
- **Frameworks (FastAPI/Pydantic) espalhados por todas as camadas**
- **Dependências explícitas entre camadas**

---

## Depois (Hexagonal)

```
src/
├── domain/                             # ⭐ NÚCLEO PURO
│   ├── entities/
│   │   └── product.py                  # Entidade (dataclass, sem Pydantic)
│   ├── exceptions/
│   │   └── product_exceptions.py       # Exceções de domínio
│   └── ports/                          # Interfaces (contratos)
│       ├── input/
│       │   └── product_use_case.py     # Input Port (interface)
│       └── output/
│           └── product_repository.py   # Output Port (interface)
│
├── application/                        # ⭐ CASOS DE USO
│   └── use_cases/
│       └── product_use_case.py        # Implementa Input Port
│
├── infrastructure/                     # ⭐ ADAPTERS (implementações)
│   ├── di/
│   │   └── container.py               # DI manual (sem framework)
│   ├── input/
│   │   └── http/
│   │       └── fastapi/
│   │           ├── main.py             # Factory do app FastAPI
│   │           ├── handlers.py         # Exception handlers
│   │           ├── middleware.py       # Logging middleware
│   │           ├── routes/
│   │           │   ├── products.py     # Input Adapter HTTP
│   │           │   └── health.py
│   │           └── schemas/
│   │               ├── product_schemas.py  # Pydantic schemas (entrada/saída HTTP)
│   │               └── health_schemas.py   # Health check schema
│   └── output/
│       └── persistence/
│           └── in_memory/
│               └── product_repository.py  # Output Adapter
│
├── shared/                             # ⭐ COMPARTILHADO
│   ├── settings.py                     # Configurações (pydantic-settings)
│   ├── exceptions.py                   # Exceção base ApplicationServiceError
│   └── logger.py                       # Logger (structlog) com correlation ID
│
└── main.py                             # Entry point
```

---

## 📋 Mapeamento Detalhado: O que mudou?

| Antes (MVC) | Depois (Hexagonal) | Por quê? |
|-------------|-------------------|----------|
| `models/product.py` (Pydantic) | `domain/entities/product.py` (dataclass) + `infrastructure/.../schemas/product_schemas.py` (Pydantic) | **Separamos** a entidade de negócio (pura, sem framework) dos schemas Pydantic (contrato da API). O domínio não sabe que existe FastAPI ou Pydantic. |
| `services/product_service.py` | `application/use_cases/product_use_case.py` | **Renomeado** para "Use Case" (caso de uso). Implementa a interface `IProductUseCase` definida no domínio. |
| `controllers/product_controller.py` | ❌ **Removido** | O controller era uma camada intermediária desnecessária. Hoje as **rotas chamam diretamente o Use Case** (via DI). |
| `repositories/interfaces/product_repository.py` | `domain/ports/output/product_repository.py` | **Movido** para o domínio. A interface (Port) pertence ao domínio, não à infraestrutura. |
| `repositories/in_memory/in_memory_product_repository.py` | `infrastructure/output/persistence/in_memory/product_repository.py` | **Movido** para infrastructure. A implementação concreta é um Adapter. |
| `routes/products/get.py`, `post.py`, etc. | `infrastructure/input/http/fastapi/routes/products.py` | **Consolidado** em um único arquivo. Agora é um Input Adapter. |
| `factories/product_factory.py` | `infrastructure/di/container.py` | **Substituído** por injeção de dependência manual via `app.state` + `Depends`. |
| `core/settings/` | `shared/settings.py` | **Achatado** para um único arquivo em `shared/`. |
| `core/exceptions/` | `shared/exceptions.py` + `infrastructure/input/http/fastapi/handlers.py` | **Separado**: exceções base no `shared/`, handlers HTTP na infraestrutura. |
| `core/middleware/` | `infrastructure/input/http/fastapi/middleware.py` | **Movido** para a infraestrutura, junto ao framework que serve. |

---

## 🧭 Regra de Ouro: Dependências

A regra mais importante da Arquitetura Hexagonal:

```
📥 INFRASTRUCTURE → APPLICATION → DOMAIN (sem dependências)
📤 DOMAIN ← APPLICATION ← INFRASTRUCTURE
```

- **Domain**: Não importa NADA de fora. Zero dependências externas.
- **Application**: Importa apenas do Domain (e de bibliotecas padrão Python).
- **Infrastructure**: Importa de Application e Domain (e de frameworks/bibliotecas).
- **Shared**: Pode ser importado por qualquer camada (cross-cutting).

### Exemplo Prático:

```python
# ✅ CERTO: Domain entity sem dependências externas
@dataclass
class Product:
    id: UUID
    name: str
    price: float

# ❌ ERRADO: Domain entity com Pydantic/FastAPI
from pydantic import BaseModel  # NÃO! Domínio não pode depender de framework

# ✅ CERTO: Input Port no Domain
class IProductUseCase(ABC):
    @abstractmethod
    async def create_product(self, name: str, price: float) -> Product: ...

# ✅ CERTO: Use Case na Application depende apenas da Port
class ProductUseCase(IProductUseCase):
    def __init__(self, repository: IProductRepository):  # Depende da interface!
        self._repository = repository
```

---

## 🤔 Para Iniciantes: Analogia do Restaurante

Pense na Arquitetura Hexagonal como um **restaurante**:

| Camada Hexagonal | Analogia | O que faz? |
|-----------------|----------|------------|
| **Domain** | 🧑‍🍳 **A cozinha (receitas)** | As regras de negócio puras. Como preparar um prato. |
| **Application** | 📋 **O gerente** | Coordena o pedido, chama a cozinha, entrega o prato. |
| **Infrastructure (Input)** | 🎤 **O garçom** | Recebe o pedido do cliente (HTTP, CLI, eventos) e repassa ao gerente. |
| **Infrastructure (Output)** | 🚚 **O fornecedor** | Busca ingredientes no estoque (banco de dados, APIs externas). |
| **Ports** | 📞 **O telefone do restaurante** | Contratos/interfaces que definem COMO se comunicar. |
| **Shared** | 🔧 **Manutenção** | Coisas que todo mundo usa (luz, água, sistema de som). |

**Vantagem**: Se você trocar o garçom (HTTP → GraphQL) ou o fornecedor (SQL → MongoDB), a cozinha (domínio) continua funcionando sem alterações!

---

## 🔄 Fluxo Completo de uma Requisição

```
Cliente (HTTP)
    │
    ▼
┌─────────────────────────────────────────────┐
│ INFRASTRUCTURE (Input Adapter)              │
│   POST /api/v1/products/                    │
│   → Valida dados (ProductCreateSchema)       │
│   → Chama Use Case                          │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ APPLICATION (Use Case)                      │
│   → Verifica se nome já existe               │
│   → Cria entidade Product                    │
│   → Salva via Repository Port                │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ DOMAIN (Entity + Port Interface)            │
│   Product.create() → regra de negócio pura  │
│   IProductRepository.save() → contrato      │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ INFRASTRUCTURE (Output Adapter)             │
│   InMemoryProductRepository.save()          │
│   → Implementa a interface IProductRepository│
└─────────────────────────────────────────────┘
```

---

## ✅ Benefícios que Você Tem Agora

- ✅ **Domínio puro** — sem dependência de FastAPI, Pydantic ou banco de dados
- ✅ **Testabilidade** — Use Case testado com mock do repositório
- ✅ **Troca de banco de dados** — Basta criar um novo Adapter SQL implementando `IProductRepository`
- ✅ **Troca de framework** — O domínio não sabe se você usa FastAPI, Django ou Flask
- ✅ **Injeção de Dependência** — manual via `app.state` + `Depends` (sem frameworks de DI)
- ✅ **Separação clara** — Cada camada tem uma responsabilidade bem definida
