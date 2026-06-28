"""Shared Pydantic models: pagination and generic helpers."""
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_by: str = "created_at"
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    page_size: int
    items: list[T]


class MessageResponse(BaseModel):
    message: str


class UserBrief(BaseModel):
    """Compact user reference embedded in other responses."""

    model_config = {"from_attributes": True}

    id: int
    username: str
