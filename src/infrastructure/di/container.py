from fastapi import Request

from src.application.use_cases.product_use_case import ProductUseCase
from src.domain.ports.input.product_use_case import IProductUseCase
from src.domain.ports.output.product_repository import IProductRepository


def get_product_use_case(request: Request) -> IProductUseCase:
    return request.app.state.product_use_case


def build_product_use_case(repo: IProductRepository) -> IProductUseCase:
    return ProductUseCase(repo)
