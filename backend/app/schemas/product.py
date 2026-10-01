from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    sku: str = Field(min_length=1, max_length=50)
    description: str | None = None
    category_id: int
    item_type: str = Field(default="CONSUMABLE", max_length=20)
    unit_price: Decimal = Field(ge=0)
    cost_price: Decimal = Field(ge=0)
    current_stock: int = Field(default=0, ge=0)
    minimum_stock: int = Field(default=0, ge=0)
    unit: str = Field(min_length=1, max_length=30)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    category_id: int | None = None
    item_type: str | None = Field(default=None, max_length=20)
    unit_price: Decimal | None = Field(default=None, ge=0)
    cost_price: Decimal | None = Field(default=None, ge=0)
    minimum_stock: int | None = Field(default=None, ge=0)
    unit: str | None = Field(default=None, min_length=1, max_length=30)
    is_active: bool | None = None


class ProductResponse(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)