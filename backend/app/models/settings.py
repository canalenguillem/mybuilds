"""Application settings schemas (integrations configured from the dashboard)."""
from __future__ import annotations

from pydantic import BaseModel


class IntegrationSettings(BaseModel):
    """Never returns the raw key — only whether it's set and a masked preview."""

    openai_configured: bool
    openai_key_masked: str | None = None
    openai_model: str
    openai_source: str  # "database" | "environment" | "none"


class IntegrationSettingsUpdate(BaseModel):
    # Send a new key to set it, "" to clear it back to the env fallback, or omit
    # to leave it unchanged.
    openai_api_key: str | None = None
    openai_model: str | None = None


class IntegrationTestResult(BaseModel):
    ok: bool
    message: str
