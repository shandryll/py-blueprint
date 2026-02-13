from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.controllers.product_controller import ProductController
from src.factories import make_product_controller
from src.models.product import ProductResponse, ProductUpdate

router = APIRouter()


@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    controller: ProductController = Depends(make_product_controller),
) -> ProductResponse:
    """Atualiza um produto existente."""
    return await controller.update(product_id, product_data)
