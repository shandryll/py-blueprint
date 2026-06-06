from uuid import UUID

from src.domain.entities.product import Product
from src.domain.ports.output.product_repository import IProductRepository


class InMemoryProductRepository(IProductRepository):
    def __init__(self) -> None:
        self._products: dict[UUID, Product] = {}

    async def save(self, product: Product) -> Product:
        self._products[product.id] = product
        return product

    async def get_by_id(self, product_id: UUID) -> Product | None:
        return self._products.get(product_id)

    async def get_by_name(self, name: str) -> Product | None:
        name_lower = name.lower()
        for p in self._products.values():
            if p.name.lower() == name_lower:
                return p
        return None

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Product]:
        items = list(self._products.values())
        return items[skip : skip + limit]

    async def count(self) -> int:
        return len(self._products)

    async def delete(self, product_id: UUID) -> bool:
        if product_id not in self._products:
            return False
        del self._products[product_id]
        return True
