"""Lightweight audit logging into the audit_log table."""
from typing import Any

from sqlalchemy.orm import Session

from app.database.models.common import AuditLog


def record(
    db: Session,
    *,
    user_id: int | None,
    action: str,
    resource_type: str | None = None,
    resource_id: int | None = None,
    changes: dict[str, Any] | None = None,
) -> None:
    """Append an audit entry. Caller is responsible for committing."""
    db.add(
        AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes=changes,
        )
    )
