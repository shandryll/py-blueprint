from fastapi import APIRouter, status

from src.factories import make_product_controller
from src.models.product import ProductCreate, ProductResponse

router = APIRouter()


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate) -> ProductResponse:
    """Cria um novo produto."""
    controller = make_product_controller()
    return await controller.create(product_data)
