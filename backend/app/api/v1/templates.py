"""Template management routes."""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.models.users import ROLE_ADMIN, ROLE_OPERATOR, User
from app.database.session import get_db
from app.dependencies import get_current_user, require_roles
from app.models.common import MessageResponse, PaginationParams, UserBrief
from app.models.templates import (
    ReorderRequest,
    ReorderResponse,
    TemplateCreate,
    TemplateCreatedResponse,
    TemplateDetail,
    TemplateListResponse,
    TemplateUpdate,
    TemplateUpdatedResponse,
)
from app.services.template_service import TemplateService

router = APIRouter(prefix="/templates", tags=["Templates"])

writer = require_roles(ROLE_ADMIN, ROLE_OPERATOR)


@router.post("", response_model=TemplateCreatedResponse, status_code=status.HTTP_201_CREATED)
def create_template(
    data: TemplateCreate, db: Session = Depends(get_db), user: User = Depends(writer)
) -> TemplateCreatedResponse:
    tpl = TemplateService(db).create(data, user.id)
    return TemplateCreatedResponse(
        id=tpl.id, name=tpl.name, product_id=tpl.product_id, version=tpl.version,
        is_active=tpl.is_active, section_count=len(tpl.sections),
        created_by=UserBrief(id=user.id, username=user.username), created_at=tpl.created_at,
    )


@router.get("", response_model=TemplateListResponse)
def list_templates(
    product_id: int | None = None,
    consultant_id: str | None = None,
    is_active: bool | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> TemplateListResponse:
    pagination = PaginationParams(page=page, page_size=page_size)
    return TemplateService(db).list(pagination, product_id, consultant_id, is_active)


@router.get("/{template_id}", response_model=TemplateDetail)
def get_template(
    template_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> TemplateDetail:
    return TemplateService(db).detail(template_id)


@router.put("/{template_id}", response_model=TemplateUpdatedResponse)
def update_template(
    template_id: int,
    data: TemplateUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(writer),
) -> TemplateUpdatedResponse:
    tpl = TemplateService(db).update(template_id, data, user.id)
    return TemplateUpdatedResponse(
        id=tpl.id, name=tpl.name, version=tpl.version, updated_at=tpl.updated_at
    )


@router.post("/{template_id}/sections/reorder", response_model=ReorderResponse)
def reorder_sections(
    template_id: int,
    data: ReorderRequest,
    db: Session = Depends(get_db),
    user: User = Depends(writer),
) -> ReorderResponse:
    return TemplateService(db).reorder(template_id, data, user.id)


@router.delete("/{template_id}", response_model=MessageResponse)
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(ROLE_ADMIN)),
) -> MessageResponse:
    TemplateService(db).delete(template_id)
    return MessageResponse(message="Template deleted successfully")
