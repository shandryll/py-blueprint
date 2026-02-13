from uuid import UUID

from fastapi import APIRouter, Query, status

from src.factories import make_product_controller
from src.models.product import ProductResponse

router = APIRouter()


@router.get("/", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
async def get_all_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> list[ProductResponse]:
    """Lista todos os produtos."""
    controller = make_product_controller()
    return await controller.get_all(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_product(product_id: UUID) -> ProductResponse:
    """Busca um produto por ID."""
    controller = make_product_controller()
    return await controller.get_by_id(product_id)
