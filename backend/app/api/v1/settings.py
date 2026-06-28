"""Application settings routes (integrations: OpenAI key/model)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings as env_settings
from app.database.models.users import ROLE_ADMIN, User
from app.database.session import get_db
from app.dependencies import get_current_user, require_roles
from app.models.settings import (
    IntegrationSettings,
    IntegrationSettingsUpdate,
    IntegrationTestResult,
)
from app.services import settings_service
from app.services.ai_service import AIService

router = APIRouter(prefix="/settings", tags=["Settings"])


def _current(db: Session) -> IntegrationSettings:
    db_key = settings_service.get(db, settings_service.KEY_OPENAI_API_KEY)
    api_key, model = settings_service.get_openai_config(db)
    source = "database" if db_key else ("environment" if env_settings.openai_api_key else "none")
    return IntegrationSettings(
        openai_configured=bool(api_key),
        openai_key_masked=settings_service.mask_key(api_key),
        openai_model=model,
        openai_source=source,
    )


@router.get("/integrations", response_model=IntegrationSettings)
def get_integrations(
    db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> IntegrationSettings:
    return _current(db)


@router.put("/integrations", response_model=IntegrationSettings)
def update_integrations(
    data: IntegrationSettingsUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(ROLE_ADMIN)),
) -> IntegrationSettings:
    if data.openai_api_key is not None:
        # Empty string clears the override (falls back to env); otherwise store.
        settings_service.set_value(
            db, settings_service.KEY_OPENAI_API_KEY, data.openai_api_key or None
        )
    if data.openai_model is not None:
        settings_service.set_value(
            db, settings_service.KEY_OPENAI_MODEL, data.openai_model or None
        )
    db.commit()
    return _current(db)


@router.post("/integrations/test", response_model=IntegrationTestResult)
def test_integrations(
    db: Session = Depends(get_db), _: User = Depends(require_roles(ROLE_ADMIN))
) -> IntegrationTestResult:
    api_key, model = settings_service.get_openai_config(db)
    ok, message = AIService(api_key=api_key, model=model).test_connection()
    return IntegrationTestResult(ok=ok, message=message)
