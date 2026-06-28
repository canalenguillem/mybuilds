"""Template request/response schemas (match API_SPECIFICATIONS.md)."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.common import UserBrief

SECTION_TYPES = ("static_document", "dynamic_compliance", "custom_html")
TEMPLATE_TYPES = ("product_generic", "consultant_specific", "custom")


class SectionInput(BaseModel):
    section_name: str = Field(min_length=1, max_length=255)
    section_order: int = Field(ge=1)
    section_type: str = "static_document"
    description: str | None = None
    document_ids: list[int] = []
    is_mandatory: bool = True
    is_editable: bool = False


class TemplateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    product_id: int | None = None
    consultant_id: str | None = Field(default=None, max_length=100)
    template_type: str | None = "product_generic"
    branding_config: dict[str, Any] | None = None
    header_footer_config: dict[str, Any] | None = None
    sections: list[SectionInput] = []


class TemplateUpdate(TemplateCreate):
    """Same shape as create; a full replace that bumps the version."""


class TemplateCreatedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    product_id: int | None = None
    version: int
    is_active: bool
    section_count: int
    created_by: UserBrief
    created_at: datetime


class TemplateUpdatedResponse(BaseModel):
    id: int
    name: str
    version: int
    updated_at: datetime


class TemplateListItem(BaseModel):
    id: int
    name: str
    product_id: int | None = None
    consultant_id: str | None = None
    template_type: str | None = None
    version: int
    section_count: int
    is_active: bool
    last_updated: datetime


class TemplateListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    templates: list[TemplateListItem]


class SectionDocumentBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    file_size: int | None = None


class SectionDetail(BaseModel):
    id: int
    section_name: str
    section_order: int
    section_type: str | None = None
    description: str | None = None
    document_ids: list[int] = []
    is_mandatory: bool
    is_editable: bool
    documents: list[SectionDocumentBrief] = []


class TemplateDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    product_id: int | None = None
    consultant_id: str | None = None
    template_type: str | None = None
    version: int
    is_active: bool
    branding_config: dict[str, Any] | None = None
    header_footer_config: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime
    sections: list[SectionDetail] = []


class ReorderItem(BaseModel):
    section_id: int
    new_order: int = Field(ge=1)


class ReorderRequest(BaseModel):
    sections: list[ReorderItem] = Field(min_length=1)


class ReorderedSection(BaseModel):
    section_id: int
    section_name: str
    new_order: int


class ReorderResponse(BaseModel):
    message: str
    template_id: int
    sections: list[ReorderedSection]
