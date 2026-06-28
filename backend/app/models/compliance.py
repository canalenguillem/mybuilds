"""Compliance request/response schemas (match API_SPECIFICATIONS.md)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.common import UserBrief

REVIEW_STATUSES = ("pending_review", "reviewed", "approved", "rejected", "needs_revision")


class AnalyzeRequest(BaseModel):
    consultant_requirements_doc_id: int
    product_ids: list[int] = Field(min_length=1)
    submittal_id: int | None = None


class AnalyzeResponse(BaseModel):
    task_id: str
    message: str
    estimated_time_seconds: int
    status_url: str


class ComplianceTaskStatus(BaseModel):
    task_id: str
    status: str
    progress: int
    message: str
    requirements_found: int | None = None
    statements_generated: int | None = None
    ai_model: str | None = None


class StatementListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    submittal_id: int | None = None
    requirement_id: int | None = None
    statement: str
    confidence_score: float | None = None
    is_ai_generated: bool
    review_status: str
    created_at: datetime


class StatementListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    statements: list[StatementListItem]


class ReviewRequest(BaseModel):
    review_status: str = Field(pattern="^(approved|rejected|needs_revision)$")
    review_notes: str | None = None
    revised_statement: str | None = None


class ReviewResponse(BaseModel):
    id: int
    review_status: str
    reviewed_by: UserBrief
    reviewed_at: datetime
    review_notes: str | None = None


class RequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_document_id: int | None = None
    source_document_name: str | None = None
    requirement_text: str
    requirement_category: str | None = None
    extracted_keywords: list | None = None
    ai_extraction_confidence: float | None = None
    extracted_at: datetime
