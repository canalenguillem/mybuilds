"""Standard error response envelope (see API_SPECIFICATIONS.md)."""
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    request_id: str | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
