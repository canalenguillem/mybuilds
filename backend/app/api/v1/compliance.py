"""AI compliance analysis and review routes."""
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models.users import ROLE_ADMIN, ROLE_OPERATOR, ROLE_REVIEWER, User
from app.database.session import get_db
from app.dependencies import get_current_user, require_roles
from app.models.common import PaginationParams
from app.models.compliance import (
    AnalyzeRequest,
    AnalyzeResponse,
    ComplianceTaskStatus,
    RequirementResponse,
    ReviewRequest,
    ReviewResponse,
    StatementListResponse,
)
from app.services.compliance_service import ComplianceService
from app.tasks.celery_app import celery_app
from app.tasks.compliance_analysis import analyze_compliance

router = APIRouter(prefix="/compliance", tags=["Compliance"])


@router.post("/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_202_ACCEPTED)
def analyze(
    data: AnalyzeRequest,
    _: User = Depends(require_roles(ROLE_ADMIN, ROLE_OPERATOR)),
) -> AnalyzeResponse:
    task = analyze_compliance.delay(
        data.consultant_requirements_doc_id, data.product_ids, data.submittal_id
    )
    return AnalyzeResponse(
        task_id=task.id,
        message="Compliance analysis started",
        estimated_time_seconds=60,
        status_url=f"{settings.api_v1_prefix}/compliance/tasks/{task.id}",
    )


@router.get("/tasks/{task_id}", response_model=ComplianceTaskStatus)
def task_status(task_id: str, _: User = Depends(get_current_user)) -> ComplianceTaskStatus:
    res = AsyncResult(task_id, app=celery_app)
    info = res.info if isinstance(res.info, dict) else {}
    mapping = {
        "PENDING": ("pending", 0, "Queued"),
        "STARTED": ("processing", 5, "Started"),
        "PROGRESS": ("processing", info.get("progress", 0), info.get("message", "Processing")),
        "SUCCESS": ("completed", 100, "Compliance analysis complete"),
        "FAILURE": ("failed", 0, "Analysis failed"),
    }
    state, progress, message = mapping.get(res.state, ("processing", info.get("progress", 0), "Processing"))
    return ComplianceTaskStatus(
        task_id=task_id, status=state, progress=progress, message=message,
        requirements_found=info.get("requirements_found"),
        statements_generated=info.get("statements_generated"),
        ai_model=info.get("ai_model"),
    )


@router.get("/statements", response_model=StatementListResponse)
def list_statements(
    submittal_id: int | None = None,
    review_status: str | None = None,
    confidence_score_min: float | None = Query(None, ge=0, le=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> StatementListResponse:
    pagination = PaginationParams(page=page, page_size=page_size)
    return ComplianceService(db).list_statements(
        pagination, submittal_id, review_status, confidence_score_min
    )


@router.post("/statements/{statement_id}/review", response_model=ReviewResponse)
def review_statement(
    statement_id: int,
    data: ReviewRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(ROLE_ADMIN, ROLE_REVIEWER)),
) -> ReviewResponse:
    return ComplianceService(db).review(statement_id, data, user)


@router.get("/requirements/{requirement_id}", response_model=RequirementResponse)
def get_requirement(
    requirement_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> RequirementResponse:
    return RequirementResponse.model_validate(
        ComplianceService(db).get_requirement(requirement_id)
    )
