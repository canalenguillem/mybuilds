"""Submittal generation and management routes."""
import os

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models.users import ROLE_ADMIN, ROLE_OPERATOR, User
from app.database.session import get_db
from app.dependencies import get_current_user, require_roles
from app.exceptions import NotFoundError
from app.models.submittals import (
    GenerateRequest,
    GenerateResponse,
    SubmittalDeleteResponse,
    SubmittalDetail,
    SubmittalListResponse,
    TaskStatusResponse,
)
from app.models.common import PaginationParams
from app.services.submittal_service import SubmittalService
from app.tasks.celery_app import celery_app
from app.tasks.pdf_generation import generate_submittal

router = APIRouter(prefix="/submittals", tags=["Submittals"])

writer = require_roles(ROLE_ADMIN, ROLE_OPERATOR)


@router.post("/generate", response_model=GenerateResponse, status_code=status.HTTP_202_ACCEPTED)
def generate(
    data: GenerateRequest, db: Session = Depends(get_db), user: User = Depends(writer)
) -> GenerateResponse:
    submittal = SubmittalService(db).create_pending(data, user)
    task = generate_submittal.delay(submittal.id)
    return GenerateResponse(
        task_id=task.id,
        submittal_id=submittal.id,
        message="Submittal generation started",
        estimated_time_seconds=30,
        status_url=f"{settings.api_v1_prefix}/submittals/tasks/{task.id}",
    )


@router.get("/tasks/{task_id}", response_model=TaskStatusResponse)
def task_status(task_id: str, _: User = Depends(get_current_user)) -> TaskStatusResponse:
    res = AsyncResult(task_id, app=celery_app)
    info = res.info if isinstance(res.info, dict) else {}

    mapping = {
        "PENDING": ("pending", 0, "Queued"),
        "STARTED": ("processing", 5, "Started"),
        "PROGRESS": ("processing", info.get("progress", 0), info.get("message", "Processing")),
        "SUCCESS": ("completed", 100, "Submittal generated successfully"),
        "FAILURE": ("failed", 0, "Generation failed"),
    }
    state, progress, message = mapping.get(res.state, ("processing", info.get("progress", 0), "Processing"))
    return TaskStatusResponse(
        task_id=task_id,
        status=state,
        progress=progress,
        message=message,
        submittal_id=info.get("submittal_id"),
        file_url=info.get("file_url"),
        page_count=info.get("page_count"),
        file_size=info.get("file_size"),
    )


@router.get("", response_model=SubmittalListResponse)
def list_submittals(
    product_id: int | None = None,
    consultant_id: str | None = None,
    status_filter: str | None = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> SubmittalListResponse:
    pagination = PaginationParams(page=page, page_size=page_size)
    return SubmittalService(db).list(pagination, product_id, consultant_id, status_filter)


@router.get("/{submittal_id}", response_model=SubmittalDetail)
def get_submittal(
    submittal_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> SubmittalDetail:
    return SubmittalService(db).detail(submittal_id)


@router.get("/{submittal_id}/download")
def download(submittal_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    s = SubmittalService(db).get_or_404(submittal_id)
    if not s.generated_file_path or not os.path.exists(s.generated_file_path):
        raise NotFoundError("Generated file is not available yet.")
    return FileResponse(
        s.generated_file_path,
        media_type="application/pdf",
        filename=f"{s.submission_number}.pdf",
    )


@router.delete("/{submittal_id}", response_model=SubmittalDeleteResponse)
def archive(
    submittal_id: int, db: Session = Depends(get_db), user: User = Depends(writer)
) -> SubmittalDeleteResponse:
    archived_at = SubmittalService(db).archive(submittal_id, user.id)
    return SubmittalDeleteResponse(
        message="Submittal archived successfully", submittal_id=submittal_id, archived_at=archived_at
    )
