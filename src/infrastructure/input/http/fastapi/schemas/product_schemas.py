from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ProductCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    stock: int = Field(0, ge=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be only whitespace")
        return v.strip()


class ProductUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    price: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)

    @model_validator(mode="after")
    def at_least_one_field(self) -> "ProductUpdateSchema":
        if not any([self.name, self.description, self.price is not None, self.stock is not None]):
            raise ValueError("At least one field must be provided for update")
        return self


class ProductResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None
    price: float
    stock: int
    created_at: datetime
    updated_at: datetime | None


class PaginatedProductsResponse(BaseModel):
    items: list[ProductResponseSchema]
    total: int
    skip: int
    limit: int
