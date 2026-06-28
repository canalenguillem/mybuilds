"""Submittal request/response schemas (match API_SPECIFICATIONS.md)."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class GenerateRequest(BaseModel):
    template_id: int
    product_id: int
    consultant_id: str | None = None
    project_name: str | None = Field(default=None, max_length=255)
    project_code: str | None = Field(default=None, max_length=100)
    metadata: dict[str, Any] | None = None


class GenerateResponse(BaseModel):
    task_id: str
    submittal_id: int
    message: str
    estimated_time_seconds: int
    status_url: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str  # pending | processing | completed | failed
    progress: int
    submittal_id: int | None = None
    message: str
    file_url: str | None = None
    page_count: int | None = None
    file_size: int | None = None


class SubmittalListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    submission_number: str
    product_id: int
    template_id: int
    consultant_id: str | None = None
    project_name: str | None = None
    status: str
    page_count: int | None = None
    file_size: int | None = None
    created_at: datetime
    generated_at: datetime | None = None


class SubmittalListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    submittals: list[SubmittalListItem]


class AuditEntry(BaseModel):
    action: str | None = None
    actor: str | None = None
    timestamp: datetime


class SubmittalDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    submission_number: str
    product_id: int
    template_id: int
    consultant_id: str | None = None
    project_name: str | None = None
    project_code: str | None = None
    status: str
    page_count: int | None = None
    file_size: int | None = None
    total_sections: int | None = None
    metadata: dict[str, Any] | None = Field(default=None, alias="submittal_metadata")
    generated_at: datetime | None = None
    created_at: datetime
    audit_trail: list[AuditEntry] = []


class SubmittalDeleteResponse(BaseModel):
    message: str
    submittal_id: int
    archived_at: datetime
