"""DB-backed application settings (e.g. the client's OpenAI API key).

Settings live in the system_settings table so the client configures integrations
from the dashboard rather than via environment variables. Environment values are
used only as a fallback when a setting hasn't been saved.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings as env_settings
from app.database.models.common import SystemSetting

KEY_OPENAI_API_KEY = "openai_api_key"
KEY_OPENAI_MODEL = "openai_model"


def get(db: Session, key: str) -> str | None:
    row = db.scalar(select(SystemSetting).where(SystemSetting.setting_key == key))
    return row.setting_value if row else None


def set_value(db: Session, key: str, value: str | None, value_type: str = "string") -> None:
    row = db.scalar(select(SystemSetting).where(SystemSetting.setting_key == key))
    if row is None:
        row = SystemSetting(setting_key=key, value_type=value_type)
        db.add(row)
    row.setting_value = value


def get_openai_config(db: Session) -> tuple[str, str]:
    """Resolve (api_key, model): DB value first, then environment fallback."""
    api_key = get(db, KEY_OPENAI_API_KEY) or env_settings.openai_api_key or ""
    model = get(db, KEY_OPENAI_MODEL) or env_settings.openai_model
    return api_key, model


def mask_key(value: str | None) -> str | None:
    """Return a masked preview (e.g. sk-…ab12) — never the full secret."""
    if not value:
        return None
    if len(value) <= 8:
        return "•" * len(value)
    return f"{value[:3]}…{value[-4:]}"
