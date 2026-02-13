from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ProductBase(BaseModel):
    """Modelo base para Product.

    Contém campos comuns compartilhados entre diferentes operações.
    """

    name: str = Field(..., min_length=1, max_length=200, description="Nome do produto")
    description: str | None = Field(None, max_length=1000, description="Descrição do produto")
    price: float = Field(..., gt=0, description="Preço do produto (deve ser maior que zero)")
    stock: int = Field(0, ge=0, description="Quantidade em estoque")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Valida o nome do produto.

        Args:
            v: Nome do produto.

        Returns:
            str: Nome validado e normalizado.

        Raises:
            ValueError: Se o nome for apenas espaços em branco.
        """
        if not v.strip():
            raise ValueError("Name cannot be only whitespace")
        return v.strip()


class ProductCreate(ProductBase):
    """Modelo para criação de produto.

    Usado na validação de dados ao criar um novo produto.
    """

    pass


class ProductUpdate(BaseModel):
    """Modelo para atualização de produto.

    Todos os campos são opcionais, permitindo atualizações parciais.
    """

    name: str | None = Field(None, min_length=1, max_length=200, description="Nome do produto")
    description: str | None = Field(None, max_length=1000, description="Descrição do produto")
    price: float | None = Field(None, gt=0, description="Preço do produto")
    stock: int | None = Field(None, ge=0, description="Quantidade em estoque")


class ProductResponse(ProductBase):
    """Modelo de resposta para produto.

    Inclui campos adicionais retornados pela API (ID e timestamps).
    """

    id: UUID = Field(..., description="ID único do produto (UUID)")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime | None = Field(None, description="Data da última atualização")
