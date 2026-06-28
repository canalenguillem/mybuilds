"""Analytics / dashboard routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.models.users import User
from app.database.session import get_db
from app.dependencies import get_current_user
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> dict:
    return AnalyticsService(db).dashboard()
