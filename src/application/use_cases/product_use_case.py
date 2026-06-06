from uuid import UUID

from src.domain.entities.product import Product
from src.domain.exceptions.product_exceptions import (
    ProductNameAlreadyExistsError,
    ProductNotFoundError,
)
from src.domain.ports.input.product_use_case import IProductUseCase
from src.domain.ports.output.product_repository import IProductRepository
from src.shared.logger import get_logger

_logger = get_logger(__name__)


class ProductUseCase(IProductUseCase):
    def __init__(self, repository: IProductRepository) -> None:
        self._repository = repository

    async def create_product(
        self,
        name: str,
        price: float,
        stock: int = 0,
        description: str | None = None,
    ) -> Product:
        existing = await self._repository.get_by_name(name)
        if existing:
            raise ProductNameAlreadyExistsError(name)

        product = Product.create(
            name=name,
            price=price,
            stock=stock,
            description=description,
        )
        saved = await self._repository.save(product)
        _logger.info("product_created", product_id=str(saved.id), name=saved.name)
        return saved

    async def get_product_by_id(self, product_id: UUID) -> Product:
        product = await self._repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(str(product_id))
        return product

    async def get_product_by_name(self, name: str) -> Product:
        product = await self._repository.get_by_name(name)
        if not product:
            raise ProductNotFoundError(name)
        return product

    async def get_all_products(self, skip: int = 0, limit: int = 100) -> list[Product]:
        return await self._repository.get_all(skip=skip, limit=limit)

    async def count_products(self) -> int:
        return await self._repository.count()

    async def update_product(
        self,
        product_id: UUID,
        name: str | None = None,
        description: str | None = None,
        price: float | None = None,
        stock: int | None = None,
    ) -> Product:
        product = await self._repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(str(product_id))

        if name is not None and name != product.name:
            existing = await self._repository.get_by_name(name)
            if existing and existing.id != product_id:
                raise ProductNameAlreadyExistsError(name)

        updated = product.update(
            name=name,
            description=description,
            price=price,
            stock=stock,
        )
        saved = await self._repository.save(updated)
        _logger.info("product_updated", product_id=str(saved.id), name=saved.name)
        return saved

    async def delete_product(self, product_id: UUID) -> None:
        deleted = await self._repository.delete(product_id)
        if not deleted:
            raise ProductNotFoundError(str(product_id))
        _logger.info("product_deleted", product_id=str(product_id))
