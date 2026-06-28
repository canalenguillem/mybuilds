"""Product request/response schemas (match API_SPECIFICATIONS.md)."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    category: str | None = Field(default=None, max_length=100)
    sku: str | None = Field(default=None, max_length=100)
    vendor_id: int | None = None


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    category: str | None = Field(default=None, max_length=100)
    sku: str | None = Field(default=None, max_length=100)
    vendor_id: int | None = None
    is_active: bool | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    category: str | None = None
    sku: str | None = None
    vendor_id: int | None = None
    is_active: bool
    created_at: datetime


class ProductListItem(BaseModel):
    id: int
    name: str
    category: str | None = None
    sku: str | None = None
    is_active: bool
    document_count: int = 0
    templates_count: int = 0


class ProductListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    products: list[ProductListItem]
