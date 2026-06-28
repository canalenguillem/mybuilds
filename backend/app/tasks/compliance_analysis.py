"""Celery task for AI compliance analysis."""
from __future__ import annotations

from app.database.session import SessionLocal
from app.services.compliance_service import ComplianceService
from app.tasks.celery_app import celery_app


@celery_app.task(bind=True, name="compliance.analyze")
def analyze_compliance(
    self, requirements_doc_id: int, product_ids: list[int], submittal_id: int | None
) -> dict:
    db = SessionLocal()

    def progress(pct: int, message: str) -> None:
        self.update_state(state="PROGRESS", meta={"progress": pct, "message": message})

    try:
        progress(5, "Starting analysis")
        result = ComplianceService(db).run_analysis(
            requirements_doc_id=requirements_doc_id,
            product_ids=product_ids,
            submittal_id=submittal_id,
            progress=progress,
        )
        return {"progress": 100, "message": "Compliance analysis complete", **result}
    finally:
        db.close()
