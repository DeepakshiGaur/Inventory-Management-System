from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class AssetCreate(BaseModel):
    product_id: int
    asset_tag: str = Field(min_length=1, max_length=100)
    serial_number: str = Field(min_length=1, max_length=100)
    status: str = Field(default="AVAILABLE", max_length=30)
    condition: str = Field(default="GOOD", max_length=30)
    location: str | None = Field(default=None, max_length=150)
    purchase_date: date | None = None
    warranty_expiry: date | None = None
    notes: str | None = None


class AssetUpdate(BaseModel):
    status: str | None = Field(default=None, max_length=30)
    condition: str | None = Field(default=None, max_length=30)
    location: str | None = Field(default=None, max_length=150)
    warranty_expiry: date | None = None
    notes: str | None = None


class AssetResponse(BaseModel):
    id: int
    product_id: int
    asset_tag: str
    serial_number: str
    status: str
    condition: str
    location: str | None
    purchase_date: date | None
    warranty_expiry: date | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)