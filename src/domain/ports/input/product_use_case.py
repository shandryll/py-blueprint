from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.product import Product


class IProductUseCase(ABC):
    @abstractmethod
    async def create_product(
        self,
        name: str,
        price: float,
        stock: int = 0,
        description: str | None = None,
    ) -> Product:
        raise NotImplementedError

    @abstractmethod
    async def get_product_by_id(self, product_id: UUID) -> Product:
        raise NotImplementedError

    @abstractmethod
    async def get_product_by_name(self, name: str) -> Product:
        raise NotImplementedError

    @abstractmethod
    async def get_all_products(self, skip: int = 0, limit: int = 100) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    async def count_products(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_product(
        self,
        product_id: UUID,
        name: str | None = None,
        description: str | None = None,
        price: float | None = None,
        stock: int | None = None,
    ) -> Product:
        raise NotImplementedError

    @abstractmethod
    async def delete_product(self, product_id: UUID) -> None:
        raise NotImplementedError
