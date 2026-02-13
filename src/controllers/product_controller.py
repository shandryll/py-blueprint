from uuid import UUID

from src.models.product import ProductCreate, ProductResponse, ProductUpdate
from src.services.product_service import ProductService


class ProductController:
    def __init__(self, product_service: ProductService) -> None:
        """Inicializa o controller de produtos.

        Args:
            product_service: Serviço de produtos a ser utilizado.
        """
        self.product_service = product_service

    async def create(self, product_data: ProductCreate) -> ProductResponse:
        """Cria um novo produto.

        Args:
            product_data: Dados do produto a ser criado.

        Returns:
            ProductResponse: Produto criado.
        """
        return await self.product_service.create_product(product_data)

    async def get_by_id(self, product_id: UUID) -> ProductResponse:
        """Busca um produto por ID.

        Args:
            product_id: ID do produto.

        Returns:
            ProductResponse: Produto encontrado.
        """
        return await self.product_service.get_product_by_id(product_id)

    async def get_by_name(self, name: str) -> ProductResponse:
        """Busca um produto por nome.

        Args:
            name: Nome do produto.

        Returns:
            ProductResponse: Produto encontrado.
        """
        return await self.product_service.get_product_by_name(name)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ProductResponse]:
        """Busca todos os produtos com paginação.

        Args:
            skip: Número de produtos a pular.
            limit: Número máximo de produtos a retornar.

        Returns:
            list[ProductResponse]: Lista de produtos.
        """
        return await self.product_service.get_all_products(skip=skip, limit=limit)

    async def update(self, product_id: UUID, product_data: ProductUpdate) -> ProductResponse:
        """Atualiza um produto existente.

        Args:
            product_id: ID do produto a ser atualizado.
            product_data: Dados atualizados do produto.

        Returns:
            ProductResponse: Produto atualizado.
        """
        return await self.product_service.update_product(product_id, product_data)

    async def delete(self, product_id: UUID) -> None:
        """Deleta um produto.

        Args:
            product_id: ID do produto a ser deletado.
        """
        await self.product_service.delete_product(product_id)
