from uuid import UUID

from fastapi import APIRouter, status

from src.factories import make_product_controller
from src.models.product import ProductResponse, ProductUpdate

router = APIRouter()


@router.patch("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def patch_product(product_id: UUID, product_data: ProductUpdate) -> ProductResponse:
    """Atualiza parcialmente um produto existente."""
    controller = make_product_controller()
    return await controller.update(product_id, product_data)
