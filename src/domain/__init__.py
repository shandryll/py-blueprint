"""Domínio do Produto - Camada mais interna da Arquitetura Hexagonal.

Contém:
- Entidades (regras de negócio puras)
- Value Objects (tipos imutáveis)
- Exceções de domínio
- Ports (Interfaces/Contratos)
"""

from src.domain.entities.product import Product
from src.domain.exceptions.product_exceptions import (
    ProductDomainError,
    ProductNameAlreadyExistsError,
    ProductNotFoundError,
    ProductValidationError,
)
from src.domain.ports.input.product_use_case import IProductUseCase
from src.domain.ports.output.product_repository import IProductRepository

__all__ = [
    "Product",
    "ProductDomainError",
    "ProductNotFoundError",
    "ProductNameAlreadyExistsError",
    "ProductValidationError",
    "IProductUseCase",
    "IProductRepository",
]
