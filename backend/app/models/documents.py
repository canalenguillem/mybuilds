"""Document request/response schemas (match API_SPECIFICATIONS.md)."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.common import UserBrief


class DocumentResponse(BaseModel):
    """Returned by upload and as the base document shape."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    document_type: str
    title: str
    version: int
    file_size: int | None = None
    pages: int | None = None
    storage_location: str | None = None
    created_at: datetime
    created_by: UserBrief


class DocumentListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    document_type: str
    title: str
    version: int
    file_size: int | None = None
    created_at: datetime


class DocumentListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    documents: list[DocumentListItem]


class DocumentVersionItem(BaseModel):
    version: int
    file_size: int | None = None
    changed_by: str | None = None
    change_reason: str | None = None
    created_at: datetime


class DocumentDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    document_type: str
    title: str
    description: str | None = None
    version: int
    file_size: int | None = None
    pages: int | None = None
    checksum: str | None = None
    storage_location: str | None = None
    created_at: datetime
    versions: list[DocumentVersionItem] = []


class DocumentDeleteResponse(BaseModel):
    message: str
    document_id: int
    deleted_at: datetime


class DocumentVersionsResponse(BaseModel):
    document_id: int
    current_version: int
    versions: list[DocumentVersionItem]


# Grouped documents for GET /products/{id}/documents
class ProductDocumentBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    version: int
    file_size: int | None = None


class ProductDocumentsResponse(BaseModel):
    product_id: int
    product_name: str
    documents: dict[str, list[ProductDocumentBrief]]
