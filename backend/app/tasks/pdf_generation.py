"""Celery task that assembles a submittal PDF asynchronously."""
from __future__ import annotations

from app.database.session import SessionLocal
from app.services.submittal_service import SubmittalService
from app.tasks.celery_app import celery_app


@celery_app.task(bind=True, name="submittals.generate")
def generate_submittal(self, submittal_id: int) -> dict:
    """Generate the submittal PDF, reporting progress via task state."""
    db = SessionLocal()

    def progress(pct: int, message: str) -> None:
        self.update_state(
            state="PROGRESS",
            meta={"progress": pct, "message": message, "submittal_id": submittal_id},
        )

    try:
        progress(5, "Starting generation")
        result = SubmittalService(db).run_generation(submittal_id, progress=progress)
        return {"progress": 100, "message": "Submittal generated successfully", **result}
    finally:
        db.close()
