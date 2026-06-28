"""Document business logic: upload, listing, versioning, deletion."""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import UploadFile
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.database.models.documents import DOCUMENT_TYPES, Document, DocumentVersion
from app.database.models.users import User
from app.exceptions import BadRequestError, NotFoundError
from app.models.common import PaginationParams
from app.models.documents import (
    DocumentDetail,
    DocumentListItem,
    DocumentListResponse,
    DocumentVersionItem,
    DocumentVersionsResponse,
)
from app.services import audit_service
from app.services.product_service import ProductService
from app.services.storage_service import StorageService


class DocumentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.storage = StorageService()

    def get_or_404(self, document_id: int) -> Document:
        doc = self.db.get(Document, document_id)
        if not doc:
            raise NotFoundError(f"Document {document_id} was not found.")
        return doc

    @staticmethod
    def _validate_type(document_type: str) -> None:
        if document_type not in DOCUMENT_TYPES:
            raise BadRequestError(
                f"Invalid document_type '{document_type}'.",
                {"field": "document_type", "allowed": list(DOCUMENT_TYPES)},
            )

    def upload(
        self,
        *,
        upload: UploadFile,
        product_id: int,
        document_type: str,
        title: str,
        description: str | None,
        user: User,
    ) -> Document:
        self._validate_type(document_type)
        ProductService(self.db).get_or_404(product_id)  # 404 if product missing

        stored = self.storage.save(upload, product_id)
        doc = Document(
            product_id=product_id,
            document_type=document_type,
            title=title,
            description=description,
            file_path=stored.file_path,
            file_size=stored.file_size,
            file_extension=stored.file_extension,
            storage_location=stored.storage_location,
            original_filename=stored.original_filename,
            version=1,
            is_current_version=True,
            checksum=stored.checksum,
            pages=stored.pages,
            created_by=user.id,
        )
        self.db.add(doc)
        self.db.flush()

        self.db.add(
            DocumentVersion(
                document_id=doc.id, version=1, file_path=stored.file_path,
                file_size=stored.file_size, changed_by=user.id, change_reason="Initial upload",
            )
        )
        audit_service.record(
            self.db, user_id=user.id, action="document.uploaded",
            resource_type="document", resource_id=doc.id,
        )
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def add_version(
        self, document_id: int, upload: UploadFile, change_reason: str | None, user: User
    ) -> Document:
        doc = self.get_or_404(document_id)
        stored = self.storage.save(upload, doc.product_id)

        doc.version += 1
        doc.file_path = stored.file_path
        doc.file_size = stored.file_size
        doc.file_extension = stored.file_extension
        doc.checksum = stored.checksum
        doc.pages = stored.pages
        doc.original_filename = stored.original_filename
        doc.is_current_version = True

        self.db.add(
            DocumentVersion(
                document_id=doc.id, version=doc.version, file_path=stored.file_path,
                file_size=stored.file_size, changed_by=user.id,
                change_reason=change_reason or f"Version {doc.version}",
            )
        )
        audit_service.record(
            self.db, user_id=user.id, action="document.version_added",
            resource_type="document", resource_id=doc.id, changes={"version": doc.version},
        )
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def delete(self, document_id: int, user_id: int) -> datetime:
        doc = self.get_or_404(document_id)
        paths = [v.file_path for v in doc.versions if v.file_path]
        paths.append(doc.file_path)
        audit_service.record(
            self.db, user_id=user_id, action="document.deleted",
            resource_type="document", resource_id=doc.id,
        )
        self.db.delete(doc)
        self.db.commit()
        for path in set(paths):
            self.storage.delete(path)
        return datetime.now(timezone.utc)

    def list(
        self,
        pagination: PaginationParams,
        product_id: int | None = None,
        document_type: str | None = None,
        search: str | None = None,
    ) -> DocumentListResponse:
        filters = []
        if product_id is not None:
            filters.append(Document.product_id == product_id)
        if document_type:
            filters.append(Document.document_type == document_type)
        if search:
            like = f"%{search}%"
            filters.append(
                or_(
                    Document.title.like(like),
                    Document.original_filename.like(like),
                    Document.extracted_text.like(like),
                )
            )

        total = self.db.scalar(select(func.count()).select_from(Document).where(*filters)) or 0
        rows = self.db.scalars(
            select(Document)
            .where(*filters)
            .order_by(Document.created_at.desc())
            .offset(pagination.offset)
            .limit(pagination.page_size)
        ).all()

        return DocumentListResponse(
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            documents=[DocumentListItem.model_validate(d) for d in rows],
        )

    def detail(self, document_id: int) -> DocumentDetail:
        doc = self.get_or_404(document_id)
        return DocumentDetail(
            id=doc.id, product_id=doc.product_id, document_type=doc.document_type,
            title=doc.title, description=doc.description, version=doc.version,
            file_size=doc.file_size, pages=doc.pages, checksum=doc.checksum,
            storage_location=doc.storage_location, created_at=doc.created_at,
            versions=self._version_items(doc),
        )

    def versions(self, document_id: int) -> DocumentVersionsResponse:
        doc = self.get_or_404(document_id)
        return DocumentVersionsResponse(
            document_id=doc.id, current_version=doc.version, versions=self._version_items(doc)
        )

    def _version_items(self, doc: Document) -> list[DocumentVersionItem]:
        # Resolve changed_by user ids to usernames in one query.
        ids = {v.changed_by for v in doc.versions}
        names = dict(
            self.db.execute(select(User.id, User.username).where(User.id.in_(ids))).all()
        ) if ids else {}
        return [
            DocumentVersionItem(
                version=v.version, file_size=v.file_size,
                changed_by=names.get(v.changed_by), change_reason=v.change_reason,
                created_at=v.created_at,
            )
            for v in sorted(doc.versions, key=lambda v: v.version, reverse=True)
        ]
