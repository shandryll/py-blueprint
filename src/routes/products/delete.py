from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.controllers.product_controller import ProductController
from src.factories import make_product_controller

router = APIRouter()


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    controller: ProductController = Depends(make_product_controller),
) -> None:
    """Deleta um produto."""
    await controller.delete(product_id)
