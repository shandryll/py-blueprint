from functools import lru_cache

from src.controllers.product_controller import ProductController
from src.repositories.in_memory import InMemoryProductRepository
from src.repositories.product_repository import IProductRepository
from src.services.product_service import ProductService


def make_product_repository() -> IProductRepository:
    """Cria uma instância do repositório de produtos em memória.

    Returns:
        IProductRepository: Repositório de produtos.
    """
    return InMemoryProductRepository()


@lru_cache(maxsize=1)
def make_product_service() -> ProductService:
    """Cria uma instância do serviço de produtos (singleton).

    Returns:
        ProductService: Serviço de produtos.
    """
    in_memory_repository = make_product_repository()
    return ProductService(in_memory_repository)


@lru_cache(maxsize=1)
def make_product_controller() -> ProductController:
    """Cria uma instância do controller de produtos (singleton).

    Returns:
        ProductController: Controller de produtos.
    """
    product_service = make_product_service()
    return ProductController(product_service)
