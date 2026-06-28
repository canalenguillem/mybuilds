"""Health check routes."""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import get_db

router = APIRouter(tags=["Health"])


@router.get("/health")
def health() -> dict:
    """Liveness probe — does not touch dependencies."""
    return {"status": "ok"}


@router.get("/health/ready")
def readiness(db: Session = Depends(get_db)) -> dict:
    """Readiness probe — verifies the database connection."""
    db.execute(text("SELECT 1"))
    return {"status": "ready", "database": "ok"}
