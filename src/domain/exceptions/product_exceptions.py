class ProductDomainError(Exception):
    def __init__(self, message: str, code: str) -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class ProductNotFoundError(ProductDomainError):
    def __init__(self, product_id: str) -> None:
        super().__init__(
            message=f"Product with ID {product_id} not found",
            code="PRODUCT_NOT_FOUND",
        )
        self.product_id = product_id


class ProductNameAlreadyExistsError(ProductDomainError):
    def __init__(self, name: str) -> None:
        super().__init__(
            message=f"Product with name '{name}' already exists",
            code="PRODUCT_NAME_ALREADY_EXISTS",
        )
        self.name = name


class ProductValidationError(ProductDomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, code="PRODUCT_VALIDATION_ERROR")
