from uuid import UUID

from src.core.exceptions import (
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    ApplicationServiceError,
    handle_service_errors_async,
)
from src.models.product import ProductCreate, ProductResponse, ProductUpdate
from src.repositories.interfaces.product_repository import IProductRepository
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ProductService:
    SERVICE_NAME = "ProductService"

    def __init__(self, repository: IProductRepository) -> None:
        self._repository = repository

    @handle_service_errors_async(
        service_name=SERVICE_NAME,
        error_code="CREATE_ERROR",
    )
    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        """Cria um novo produto.

        Args:
            product_data: Dados do produto a ser criado.

        Returns:
            ProductResponse: Produto criado.

        Raises:
            ApplicationServiceError: Se ocorrer algum erro durante a criação.
        """
        logger.debug("Creating product", operation="create_product")

        existing_product = await self._repository.get_by_name(product_data.name)
        if existing_product:
            raise ApplicationServiceError(
                service_name=self.SERVICE_NAME,
                message=f"Product with name '{product_data.name}' already exists",
                status_code=HTTP_409_CONFLICT,
                error_code="PRODUCT_NAME_ALREADY_EXISTS",
            )

        product = await self._repository.create(product_data)
        logger.info("Product created", operation="create_product")
        return product

    @handle_service_errors_async(service_name=SERVICE_NAME, error_code="GET_ERROR")
    async def get_product_by_id(self, product_id: UUID) -> ProductResponse:
        """Busca um produto por ID.

        Args:
            product_id: ID do produto.

        Returns:
            ProductResponse: Produto encontrado.

        Raises:
            ApplicationServiceError: Se o produto não for encontrado.
        """
        logger.debug("Fetching product", operation="get_product_by_id")
        product = await self._repository.get_by_id(product_id)
        if not product:
            raise ApplicationServiceError(
                service_name=self.SERVICE_NAME,
                message=f"Product with ID {product_id} not found",
                status_code=HTTP_404_NOT_FOUND,
                error_code="PRODUCT_NOT_FOUND",
            )
        return product

    @handle_service_errors_async(service_name=SERVICE_NAME, error_code="GET_ERROR")
    async def get_product_by_name(self, name: str) -> ProductResponse:
        """Busca um produto por nome.

        Args:
            name: Nome do produto.

        Returns:
            ProductResponse: Produto encontrado.

        Raises:
            ApplicationServiceError: Se o produto não for encontrado.
        """
        logger.debug("Fetching product", operation="get_product_by_name", name=name)
        product = await self._repository.get_by_name(name)
        if not product:
            raise ApplicationServiceError(
                service_name=self.SERVICE_NAME,
                message=f"Product with name '{name}' not found",
                status_code=HTTP_404_NOT_FOUND,
                error_code="PRODUCT_NOT_FOUND",
            )
        return product

    @handle_service_errors_async(service_name=SERVICE_NAME, error_code="GET_ALL_ERROR")
    async def get_all_products(self, skip: int = 0, limit: int = 100) -> list[ProductResponse]:
        """Busca todos os produtos com paginação.

        Args:
            skip: Número de produtos a pular.
            limit: Número máximo de produtos a retornar.

        Returns:
            list[ProductResponse]: Lista de produtos.
        """
        logger.debug("Listing products", operation="get_all_products")
        products = await self._repository.get_all(skip=skip, limit=limit)
        return products

    @handle_service_errors_async(service_name=SERVICE_NAME, error_code="UPDATE_ERROR")
    async def update_product(self, product_id: UUID, product_data: ProductUpdate) -> ProductResponse:
        """Atualiza um produto existente.

        Args:
            product_id: ID do produto a ser atualizado.
            product_data: Dados atualizados do produto.

        Returns:
            ProductResponse: Produto atualizado.

        Raises:
            ApplicationServiceError: Se o produto não for encontrado ou nome já existir.
        """
        existing_product = await self._repository.get_by_id(product_id)
        if not existing_product:
            raise ApplicationServiceError(
                service_name=self.SERVICE_NAME,
                message=f"Product with ID {product_id} not found",
                status_code=HTTP_404_NOT_FOUND,
                error_code="PRODUCT_NOT_FOUND",
            )

        if product_data.name:
            product_with_same_name = await self._repository.get_by_name(product_data.name)
            if product_with_same_name and product_with_same_name.id != product_id:
                raise ApplicationServiceError(
                    service_name=self.SERVICE_NAME,
                    message=f"Product with name '{product_data.name}' already exists",
                    status_code=HTTP_409_CONFLICT,
                    error_code="PRODUCT_NAME_ALREADY_EXISTS",
                )

        updated_product = await self._repository.update(product_id, product_data)
        if updated_product is None:
            raise ApplicationServiceError(
                service_name=self.SERVICE_NAME,
                message=f"Product with ID {product_id} not found during update",
                status_code=HTTP_404_NOT_FOUND,
                error_code="PRODUCT_NOT_FOUND",
            )
        logger.info("Product updated", operation="update_product")
        return updated_product

    @handle_service_errors_async(service_name=SERVICE_NAME, error_code="DELETE_ERROR")
    async def delete_product(self, product_id: UUID) -> None:
        """Deleta um produto.

        Args:
            product_id: ID do produto a ser deletado.

        Raises:
            ApplicationServiceError: Se o produto não for encontrado.
        """
        logger.debug("Deleting product", operation="delete_product")
        deleted = await self._repository.delete(product_id)
        if not deleted:
            raise ApplicationServiceError(
                service_name=self.SERVICE_NAME,
                message=f"Product with ID {product_id} not found",
                status_code=HTTP_404_NOT_FOUND,
                error_code="PRODUCT_NOT_FOUND",
            )
        logger.info("Product deleted", operation="delete_product")
