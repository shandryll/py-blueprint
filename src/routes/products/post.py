from fastapi import APIRouter, Depends, status

from src.controllers.product_controller import ProductController
from src.factories import make_product_controller
from src.models.product import ProductCreate, ProductResponse

router = APIRouter()


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    controller: ProductController = Depends(make_product_controller),
) -> ProductResponse:
    """Cria um novo produto."""
    return await controller.create(product_data)
