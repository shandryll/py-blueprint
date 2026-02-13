from abc import ABC, abstractmethod
from uuid import UUID

from src.models.product import ProductCreate, ProductResponse, ProductUpdate


class IProductRepository(ABC):
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ProductResponse]:
        """Busca todos os produtos com paginação.

        Args:
            skip: Número de produtos a pular.
            limit: Número máximo de produtos a retornar.

        Returns:
            list[ProductResponse]: Lista de produtos.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> ProductResponse | None:
        """Busca um produto por ID.

        Args:
            entity_id: ID do produto.

        Returns:
            ProductResponse | None: Produto encontrado ou None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> ProductResponse | None:
        """Busca um produto por nome.

        Args:
            name: Nome do produto.

        Returns:
            ProductResponse | None: Produto encontrado ou None.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, entity: ProductCreate) -> ProductResponse:
        """Cria um novo produto.

        Args:
            entity: Dados do produto a ser criado.

        Returns:
            ProductResponse: Produto criado.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity_id: UUID, entity: ProductUpdate) -> ProductResponse | None:
        """Atualiza um produto existente.

        Args:
            entity_id: ID do produto a ser atualizado.
            entity: Dados atualizados do produto.

        Returns:
            ProductResponse | None: Produto atualizado ou None se não encontrado.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        """Deleta um produto existente.

        Args:
            entity_id: ID do produto a ser deletado.

        Returns:
            bool: True se deletado, False se não encontrado.
        """
        raise NotImplementedError
