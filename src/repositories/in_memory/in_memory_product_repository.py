from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.models.product import ProductCreate, ProductResponse, ProductUpdate
from src.repositories.interfaces.product_repository import IProductRepository


class InMemoryProductRepository(IProductRepository):
    def __init__(self) -> None:
        self._products_list = []

    async def create(self, entity: ProductCreate) -> ProductResponse:
        """Cria um novo produto.

        Args:
            entity: Dados do produto a ser criado.

        Returns:
            ProductResponse: Produto criado.
        """
        now = datetime.now(UTC)
        product_id = uuid4()
        product = ProductResponse(
            **entity.model_dump(),
            id=product_id,
            created_at=now,
            updated_at=None,
        )

        self._products_list.append(product)

        return product

    async def get_by_id(self, entity_id: UUID) -> ProductResponse | None:
        """Busca um produto por ID.

        Args:
            entity_id: ID do produto.

        Returns:
            ProductResponse | None: Produto encontrado ou None.
        """
        return next((product for product in self._products_list if product.id == entity_id), None)

    async def get_by_name(self, name: str) -> ProductResponse | None:
        """Busca um produto por nome.

        Args:
            name: Nome do produto.

        Returns:
            ProductResponse | None: Produto encontrado ou None.
        """
        name_lower = name.lower()
        return next(
            (product for product in self._products_list if product.name.lower() == name_lower),
            None,
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ProductResponse]:
        """Busca todos os produtos com paginação.

        Args:
            skip: Número de produtos a pular.
            limit: Número máximo de produtos a retornar.

        Returns:
            list[ProductResponse]: Lista de produtos.
        """
        products = self._products_list
        return products[skip : skip + limit]

    async def update(self, entity_id: UUID, entity: ProductUpdate) -> ProductResponse | None:
        """Atualiza um produto existente.

        Args:
            entity_id: ID do produto a ser atualizado.
            entity: Dados atualizados do produto.

        Returns:
            ProductResponse | None: Produto atualizado ou None se não encontrado.
        """
        product = next((product for product in self._products_list if product.id == entity_id), None)
        if not product:
            return None

        update_data = entity.model_dump(exclude_unset=True)
        if update_data:
            temp_data = product.model_dump()
            temp_data.update(update_data)

            ProductResponse(**temp_data)

        updated_product = product.model_copy(update=update_data)
        updated_product.updated_at = datetime.now(UTC)

        self._products_list[self._products_list.index(product)] = updated_product
        return updated_product

    async def delete(self, entity_id: UUID) -> bool:
        """Deleta um produto.

        Args:
            entity_id: ID do produto a ser deletado.

        Returns:
            bool: True se deletado, False se não encontrado.
        """
        product = next((product for product in self._products_list if product.id == entity_id), None)
        if not product:
            return False

        self._products_list.remove(product)
        return True
