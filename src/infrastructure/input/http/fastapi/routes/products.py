from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from src.domain.ports.input.product_use_case import IProductUseCase
from src.infrastructure.di.container import get_product_use_case
from src.infrastructure.input.http.fastapi.schemas.product_schemas import (
    PaginatedProductsResponse,
    ProductCreateSchema,
    ProductResponseSchema,
    ProductUpdateSchema,
)

router = APIRouter(prefix="/api/v1/products", tags=["products"])

_product_responses = {
    404: {"description": "Product not found"},
    422: {"description": "Validation error in request body"},
}

_domain_error_responses = {
    404: {"description": "Product not found"},
    409: {"description": "Duplicate product name"},
    422: {"description": "Validation error in request body"},
}


@router.post(
    "/",
    response_model=ProductResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses=_domain_error_responses,
)
async def create_product(
    product_data: ProductCreateSchema,
    use_case: IProductUseCase = Depends(get_product_use_case),
) -> ProductResponseSchema:
    product = await use_case.create_product(
        name=product_data.name,
        price=product_data.price,
        stock=product_data.stock,
        description=product_data.description,
    )
    return ProductResponseSchema.model_validate(product)


@router.get(
    "/",
    response_model=PaginatedProductsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_products(
    use_case: IProductUseCase = Depends(get_product_use_case),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> PaginatedProductsResponse:
    products = await use_case.get_all_products(skip=skip, limit=limit)
    total = await use_case.count_products()

    return PaginatedProductsResponse(
        items=[ProductResponseSchema.model_validate(p) for p in products],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponseSchema,
    status_code=status.HTTP_200_OK,
    responses=_product_responses,
)
async def get_product(
    product_id: UUID,
    use_case: IProductUseCase = Depends(get_product_use_case),
) -> ProductResponseSchema:
    product = await use_case.get_product_by_id(product_id)
    return ProductResponseSchema.model_validate(product)


@router.put(
    "/{product_id}",
    response_model=ProductResponseSchema,
    status_code=status.HTTP_200_OK,
    responses=_domain_error_responses,
)
async def update_product(
    product_id: UUID,
    product_data: ProductCreateSchema,
    use_case: IProductUseCase = Depends(get_product_use_case),
) -> ProductResponseSchema:
    product = await use_case.update_product(
        product_id=product_id,
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
    )
    return ProductResponseSchema.model_validate(product)


@router.patch(
    "/{product_id}",
    response_model=ProductResponseSchema,
    status_code=status.HTTP_200_OK,
    responses=_domain_error_responses | {422: {"description": "At least one field must be provided for update"}},
)
async def patch_product(
    product_id: UUID,
    product_data: ProductUpdateSchema,
    use_case: IProductUseCase = Depends(get_product_use_case),
) -> ProductResponseSchema:
    product = await use_case.update_product(
        product_id=product_id,
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
    )
    return ProductResponseSchema.model_validate(product)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=_product_responses,
)
async def delete_product(
    product_id: UUID,
    use_case: IProductUseCase = Depends(get_product_use_case),
) -> None:
    await use_case.delete_product(product_id)
