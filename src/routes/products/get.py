from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from src.controllers.product_controller import ProductController
from src.factories import make_product_controller
from src.models.product import ProductResponse

router = APIRouter()


@router.get("/", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
async def get_all_products(
    controller: ProductController = Depends(make_product_controller),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> list[ProductResponse]:
    """Lista todos os produtos."""
    return await controller.get_all(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_product(
    product_id: UUID,
    controller: ProductController = Depends(make_product_controller),
) -> ProductResponse:
    """Busca um produto por ID."""
    return await controller.get_by_id(product_id)
