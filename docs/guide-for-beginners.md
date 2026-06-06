# Guia para Iniciantes — Entendendo o Projeto

Este guia explica o py-blueprint **de dentro para fora**, seguindo a direção das dependências da Arquitetura Hexagonal. Cada seção depende apenas das anteriores.

---

## 1. `src/domain/entities/product.py` — A Entidade Pura

O coração do sistema. Uma classe Python **sem nenhuma dependência externa** (sem FastAPI, sem Pydantic, sem banco de dados).

```python
@dataclass(slots=True)
class Product:
    id: UUID
    name: str
    price: float
    stock: int
```

**O que observar:**
- É uma `dataclass` pura — só dados e regras de negócio
- O método `_validate()` usa `ProductValidationError` (exceção do próprio domínio)
- `create()` é um factory method (valida antes de criar)
- `update()` retorna uma **nova instância** (imutabilidade)

> 🧠 **Para fixar:** O domínio não importa nada externo. Se um dia trocar de framework (FastAPI → Django), este arquivo não muda.

---

## 2. `src/domain/ports/output/product_repository.py` — O Contrato de Saída

Uma **interface** (Port) que define *o que* o repositório precisa fazer, sem dizer *como*.

```python
class IProductRepository(ABC):
    @abstractmethod
    async def save(self, product: Product) -> Product: ...
    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Product | None: ...
```

**O que observar:**
- Só tem `@abstractmethod` — não tem implementação
- Está dentro do `domain/` porque **o domínio define o contrato**
- A implementação concreta vem depois, na infraestrutura

---

## 3. `src/domain/ports/input/product_use_case.py` — O Contrato de Entrada

Define os casos de uso que o sistema oferece.

```python
class IProductUseCase(ABC):
    @abstractmethod
    async def create_product(self, name: str, price: float, ...) -> Product: ...
    @abstractmethod
    async def get_product_by_id(self, product_id: UUID) -> Product: ...
```

---

## 4. `src/domain/exceptions/product_exceptions.py` — Exceções de Negócio

Exceções que **fazem sentido para o negócio**, não para o sistema:

```python
class ProductNotFoundError(ProductDomainError): ...
class ProductNameAlreadyExistsError(ProductDomainError): ...
class ProductValidationError(ProductDomainError): ...
```

> 🧠 **Para fixar:** `ProductNotFoundError` é diferente de `HTTP 404`. O domínio não sabe que isso será exibido num HTTP response. Depois, o handler da infraestrutura faz o mapeamento: `ProductNotFoundError` → 404.

---

## 5. `src/application/use_cases/product_use_case.py` — O Caso de Uso

A camada de **orquestração**. Implementa `IProductUseCase` e coordena as regras de negócio.

```python
class ProductUseCase(IProductUseCase):
    def __init__(self, repository: IProductRepository) -> None:
        self._repository = repository  # Depende da INTERFACE, não da implementação
```

**O que observar:**
- Depende de `IProductRepository` (a interface), não de `InMemoryProductRepository`
- Se trocar o banco de memória por PostgreSQL, esta classe **não muda**
- Contém logs de negócio (`product_created`, `product_updated`, `product_deleted`)

---

## 6. `src/infrastructure/output/persistence/in_memory/product_repository.py` — O Adapter de Saída

Implementa `IProductRepository` de verdade. Aqui é onde os dados são salvos/buscados.

```python
class InMemoryProductRepository(IProductRepository):
    def __init__(self) -> None:
        self._products: dict[UUID, Product] = {}
```

**O que observar:**
- Implementa a interface definida no domínio (`IProductRepository`)
- Você pode criar outro adapter (`PostgresProductRepository`, `RedisProductRepository`) sem tocar no use case ou na entidade

---

## 7. `src/infrastructure/di/container.py` — A "Cola" (Injeção de Dependência)

Junta as peças. Cria o caso de uso com o repositório e disponibiliza para as rotas.

```python
def build_product_use_case(repo: IProductRepository) -> IProductUseCase:
    return ProductUseCase(repo)

def get_product_use_case(request: Request) -> IProductUseCase:
    return request.app.state.product_use_case
```

**O que observar:**
- `build_product_use_case` monta o caso de uso com um repositório
- `get_product_use_case` lê do `app.state` para injetar nas rotas via `Depends`
- Não usa `dependency-injector` nem singleton global

---

## 8. `src/infrastructure/input/http/fastapi/main.py` — A Fábrica do App

Cria a aplicação FastAPI e configura tudo: handlers, middleware, CORS, rotas, DI.

```python
def create_app() -> FastAPI:
    repo = InMemoryProductRepository()
    app.state.product_use_case = build_product_use_case(repo)
    # ... adiciona middleware, handlers, rotas
    return app
```

> 🧠 **Para fixar:** É o **único lugar** que conhece FastAPI. Se trocar de framework, só este arquivo muda.

---

## 9. `src/infrastructure/input/http/fastapi/routes/products.py` — O Adapter de Entrada

Traduz requisições HTTP em chamadas para o caso de uso.

```python
@router.post("/", status_code=201)
async def create_product(
    product_data: ProductCreateSchema,
    use_case: IProductUseCase = Depends(get_product_use_case),
) -> ProductResponseSchema:
    product = await use_case.create_product(...)
    return ProductResponseSchema.model_validate(product)
```

**O que observar:**
- Schemas Pydantic validam a entrada (`ProductCreateSchema`)
- Chama o caso de uso (que orquestra a regra de negócio)
- Converte o resultado de volta para um schema de resposta
- A rota **não tem lógica de negócio** — só traduz HTTP ↔ use case

---

## 10. `tests/unit/entities/test_product.py` — Testes da Entidade

Testam a entidade pura. Sem HTTP, sem banco, sem mock.

```python
def test_create_product_empty_name_raises() -> None:
    with pytest.raises(ProductValidationError):
        Product.create(name="", price=10.0, stock=5)
```

---

## 11. `tests/unit/use_cases/test_product_use_case.py` — Testes do Caso de Uso

Testam a orquestração com um repositório in-memory isolado.

```python
async def test_create_product_success(use_case: ProductUseCase) -> None:
    out = await use_case.create_product(name="NewProduct", price=10.0, ...)
    assert out.name == "NewProduct"
```

---

## 12. `tests/integration/test_products_api.py` — Testes da API

Testam o sistema completo via HTTP (rota → schema → use case → repositório → resposta).

```python
def test_create_product_returns_201(client: TestClient) -> None:
    response = client.post("/api/v1/products/", json={...})
    assert response.status_code == 201
```

---

## Mapa Mental

```
    DE DENTRO PARA FORA (leia nesta ordem)
    ──────────────────────────────────────

    1. domain/entities/product.py         ← regra de negócio pura
    2. domain/ports/output/*.py           ← contrato de saída (repositório)
    3. domain/ports/input/*.py            ← contrato de entrada (use case)
    4. domain/exceptions/*.py             ← exceções do negócio
            ↓
    5. application/use_cases/*.py         ← orquestração (depende das interfaces)
            ↓
    6. infrastructure/output/**/*.py      ← adapter de saída (banco, API externa)
    7. infrastructure/di/container.py     ← montagem das dependências
    8. infrastructure/input/http/main.py  ← fábrica do app FastAPI
    9. infrastructure/input/http/routes/*.py ← adapter de entrada HTTP
            ↓
    10-11-12. tests/                      ← testes (entidade → use case → API)

    🔹 Números menores = mais estáveis (nunca mudam de framework/banco)
    🔹 Números maiores = mais trocáveis (adaptam-se ao mundo externo)
```

---

## Dúvidas Comuns

**"Por que o repositório é uma interface no domínio?"**
Porque o domínio define as regras de negócio. Ele precisa dizer "preciso salvar um produto", mas **não precisa saber** se o banco é MySQL, PostgreSQL ou uma lista em memória. A interface é o contrato; a implementação vem depois.

**"E se eu criar um adapter SQL?"**
Você cria um novo arquivo em `infrastructure/output/persistence/sql/product_repository.py` implementando `IProductRepository`. Depois, em `main.py`, troca `InMemoryProductRepository()` por `PostgresProductRepository()`. O use case e o domínio **não mudam uma linha**.

**"Por que a rota não tem lógica de negócio?"**
Porque a rota é só um adapter de entrada. A regra de negócio (ex: "não pode criar produto com nome duplicado") está no use case. Se amanhã você criar uma CLI ou uma fila Kafka, a mesma regra será reusada.
