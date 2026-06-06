from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def save(self, product: Product) -> Product:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    async def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, product_id: UUID) -> bool:
        raise NotImplementedError
