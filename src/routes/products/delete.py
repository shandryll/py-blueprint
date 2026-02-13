from uuid import UUID

from fastapi import APIRouter, status

from src.factories import make_product_controller

router = APIRouter()


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: UUID) -> None:
    """Deleta um produto."""
    controller = make_product_controller()
    await controller.delete(product_id)
