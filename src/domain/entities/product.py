from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.domain.exceptions.product_exceptions import ProductValidationError


@dataclass(slots=True)
class Product:
    id: UUID
    name: str
    description: str | None
    price: float
    stock: int
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        """Validate entity after initialization."""
        self._validate()

    def _validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ProductValidationError("Product name cannot be empty or whitespace only")
        if self.price <= 0:
            raise ProductValidationError("Price must be greater than zero")
        if self.stock < 0:
            raise ProductValidationError("Stock cannot be negative")

    def update(
        self,
        name: str | None = None,
        description: str | None = None,
        price: float | None = None,
        stock: int | None = None,
    ) -> "Product":
        """Create a new instance with updated fields.

        Args:
            name: New name (optional)
            description: New description (optional)
            price: New price (optional)
            stock: New stock (optional)

        Returns:
            New Product instance with updated fields
        """
        return Product(
            id=self.id,
            name=name.strip() if name is not None else self.name,
            description=description if description is not None else self.description,
            price=price if price is not None else self.price,
            stock=stock if stock is not None else self.stock,
            created_at=self.created_at,
            updated_at=datetime.now(UTC),
        )

    @classmethod
    def create(
        cls,
        name: str,
        price: float,
        stock: int = 0,
        description: str | None = None,
    ) -> "Product":
        """Create a new product.

        Args:
            name: Product name
            price: Product price
            stock: Initial stock (default 0)
            description: Optional description

        Returns:
            New Product instance
        """
        return cls(
            id=uuid4(),
            name=name.strip(),
            description=description,
            price=price,
            stock=stock,
            created_at=datetime.now(UTC),
            updated_at=None,
        )
