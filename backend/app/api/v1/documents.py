"""Document management routes (upload, list, versions, delete)."""
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.database.models.users import ROLE_ADMIN, ROLE_OPERATOR, User
from app.database.session import get_db
from app.dependencies import get_current_user, require_roles
from app.models.common import PaginationParams, UserBrief
from app.models.documents import (
    DocumentDeleteResponse,
    DocumentDetail,
    DocumentListResponse,
    DocumentResponse,
    DocumentVersionsResponse,
)
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])

writer = require_roles(ROLE_ADMIN, ROLE_OPERATOR)


def _to_response(doc, user: User) -> DocumentResponse:
    return DocumentResponse(
        id=doc.id, product_id=doc.product_id, document_type=doc.document_type,
        title=doc.title, version=doc.version, file_size=doc.file_size, pages=doc.pages,
        storage_location=doc.storage_location, created_at=doc.created_at,
        created_by=UserBrief(id=user.id, username=user.username),
    )


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
    file: UploadFile = File(...),
    product_id: int = Form(...),
    document_type: str = Form(...),
    title: str = Form(...),
    description: str | None = Form(None),
    db: Session = Depends(get_db),
    user: User = Depends(writer),
) -> DocumentResponse:
    doc = DocumentService(db).upload(
        upload=file, product_id=product_id, document_type=document_type,
        title=title, description=description, user=user,
    )
    return _to_response(doc, user)


@router.get("", response_model=DocumentListResponse)
def list_documents(
    product_id: int | None = None,
    document_type: str | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> DocumentListResponse:
    pagination = PaginationParams(page=page, page_size=page_size)
    return DocumentService(db).list(pagination, product_id, document_type, search)


@router.get("/{document_id}", response_model=DocumentDetail)
def get_document(
    document_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> DocumentDetail:
    return DocumentService(db).detail(document_id)


@router.get("/{document_id}/versions", response_model=DocumentVersionsResponse)
def get_versions(
    document_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> DocumentVersionsResponse:
    return DocumentService(db).versions(document_id)


@router.post(
    "/{document_id}/versions",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_version(
    document_id: int,
    file: UploadFile = File(...),
    change_reason: str | None = Form(None),
    db: Session = Depends(get_db),
    user: User = Depends(writer),
) -> DocumentResponse:
    doc = DocumentService(db).add_version(document_id, file, change_reason, user)
    return _to_response(doc, user)


@router.delete("/{document_id}", response_model=DocumentDeleteResponse)
def delete_document(
    document_id: int, db: Session = Depends(get_db), user: User = Depends(writer)
) -> DocumentDeleteResponse:
    deleted_at = DocumentService(db).delete(document_id, user.id)
    return DocumentDeleteResponse(
        message="Document deleted successfully", document_id=document_id, deleted_at=deleted_at
    )
