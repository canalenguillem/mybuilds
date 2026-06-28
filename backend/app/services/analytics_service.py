"""Dashboard analytics aggregations."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.database.models.compliance import ComplianceStatement
from app.database.models.documents import Document
from app.database.models.products import Product
from app.database.models.submittals import Submittal
from app.database.models.templates import Template


class AnalyticsService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _count(self, model, *where) -> int:
        return self.db.scalar(select(func.count()).select_from(model).where(*where)) or 0

    def dashboard(self) -> dict:
        now = datetime.now(timezone.utc)
        month_filter = (
            extract("year", Submittal.created_at) == now.year,
            extract("month", Submittal.created_at) == now.month,
        )
        avg_pages = self.db.scalar(
            select(func.avg(Submittal.page_count)).where(Submittal.page_count.isnot(None))
        )

        recent = self.db.scalars(
            select(Submittal).order_by(Submittal.created_at.desc()).limit(5)
        ).all()

        return {
            "metrics": {
                "total_submittals": self._count(Submittal),
                "submittals_this_month": self._count(Submittal, *month_filter),
                "total_documents": self._count(Document),
                "total_products": self._count(Product),
                "total_templates": self._count(Template),
                "compliance_pending_review": self._count(
                    ComplianceStatement,
                    ComplianceStatement.review_status == "pending_review",
                ),
                "compliance_approved": self._count(
                    ComplianceStatement, ComplianceStatement.review_status == "approved"
                ),
                "avg_pages_per_submittal": round(float(avg_pages), 1) if avg_pages else 0,
            },
            "recent_submittals": [
                {
                    "id": s.id,
                    "submission_number": s.submission_number,
                    "project_name": s.project_name,
                    "status": s.status,
                    "page_count": s.page_count,
                    "created_at": s.created_at.isoformat(),
                }
                for s in recent
            ],
        }
