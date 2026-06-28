"""Submittal orchestration: create, dispatch, run generation, query, archive."""
from __future__ import annotations

import os
from datetime import datetime, timezone

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.database.models.compliance import ComplianceStatement
from app.database.models.documents import Document
from app.database.models.submittals import Submittal, SubmittalAudit
from app.database.models.templates import Template
from app.database.models.users import User
from app.exceptions import NotFoundError
from app.models.common import PaginationParams
from app.models.submittals import (
    AuditEntry,
    GenerateRequest,
    SubmittalDetail,
    SubmittalListItem,
    SubmittalListResponse,
)
from app.services import audit_service
from app.services.pdf_service import SectionSpec, build_submittal


class SubmittalService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_404(self, submittal_id: int) -> Submittal:
        s = self.db.get(Submittal, submittal_id)
        if not s:
            raise NotFoundError(f"Submittal {submittal_id} was not found.")
        return s

    # ── Create pending row (caller dispatches the Celery task) ──
    def create_pending(self, data: GenerateRequest, user: User) -> Submittal:
        template = self.db.get(Template, data.template_id)
        if not template:
            raise NotFoundError(f"Template {data.template_id} was not found.")

        submittal = Submittal(
            submission_number=self._next_number(),
            product_id=data.product_id,
            template_id=data.template_id,
            consultant_id=data.consultant_id or template.consultant_id,
            project_name=data.project_name,
            project_code=data.project_code,
            status="generating",
            total_sections=len(template.sections),
            submittal_metadata=data.metadata,
            created_by=user.id,
        )
        self.db.add(submittal)
        self.db.flush()
        self.db.add(
            SubmittalAudit(submittal_id=submittal.id, action="created", actor_id=user.id)
        )
        audit_service.record(
            self.db, user_id=user.id, action="submittal.created",
            resource_type="submittal", resource_id=submittal.id,
        )
        self.db.commit()
        self.db.refresh(submittal)
        return submittal

    def mark_regenerating(self, submittal_id: int, user_id: int) -> Submittal:
        s = self.get_or_404(submittal_id)
        s.status = "generating"
        self.db.add(
            SubmittalAudit(submittal_id=s.id, action="regenerated", actor_id=user_id)
        )
        self.db.commit()
        self.db.refresh(s)
        return s

    def _next_number(self) -> str:
        year = datetime.now(timezone.utc).year
        count = self.db.scalar(
            select(func.count())
            .select_from(Submittal)
            .where(extract("year", Submittal.created_at) == year)
        ) or 0
        return f"SUB-{year}-{count + 1:03d}"

    # ── Generation routine (invoked by the Celery worker) ──────
    def run_generation(self, submittal_id: int, progress=None) -> dict:
        submittal = self.get_or_404(submittal_id)
        template = self.db.get(Template, submittal.template_id)
        if not template:
            raise NotFoundError("Template for this submittal no longer exists.")

        # Resolve each section's document file paths.
        all_ids = {d for s in template.sections for d in (s.document_ids or [])}
        paths = {
            d.id: d.file_path
            for d in self.db.scalars(select(Document).where(Document.id.in_(all_ids)))
        } if all_ids else {}

        # Approved compliance statements linked to this submittal, for dynamic sections.
        approved_statements = self.db.scalars(
            select(ComplianceStatement.statement).where(
                ComplianceStatement.submittal_id == submittal.id,
                ComplianceStatement.review_status == "approved",
            )
        ).all()

        specs = []
        for s in sorted(template.sections, key=lambda s: s.section_order):
            section_type = s.section_type or "static_document"
            specs.append(
                SectionSpec(
                    name=s.section_name,
                    section_type=section_type,
                    doc_paths=[paths[d] for d in (s.document_ids or []) if d in paths],
                    statements=list(approved_statements)
                    if section_type == "dynamic_compliance"
                    else [],
                )
            )

        output_path = os.path.join(
            settings.generated_pdfs_path, f"{submittal.submission_number}.pdf"
        )
        try:
            result = build_submittal(
                output_path=output_path,
                submission_number=submittal.submission_number,
                title=template.name,
                project_name=submittal.project_name,
                consultant_id=submittal.consultant_id,
                branding=template.branding_config,
                sections=specs,
                progress=progress,
            )
        except Exception:
            submittal.status = "failed"
            self.db.commit()
            raise

        submittal.status = "generated"
        submittal.generated_file_path = result.output_path
        submittal.file_size = result.file_size
        submittal.page_count = result.page_count
        submittal.generated_at = datetime.now(timezone.utc)
        self.db.add(
            SubmittalAudit(
                submittal_id=submittal.id, action="generated", actor_id=submittal.created_by,
                action_details={"page_count": result.page_count},
            )
        )
        self.db.commit()
        return {
            "submittal_id": submittal.id,
            "page_count": result.page_count,
            "file_size": result.file_size,
            "file_url": f"{settings.api_v1_prefix}/submittals/{submittal.id}/download",
        }

    # ── Queries ────────────────────────────────────────────────
    def list(
        self,
        pagination: PaginationParams,
        product_id: int | None = None,
        consultant_id: str | None = None,
        status: str | None = None,
    ) -> SubmittalListResponse:
        filters = []
        if product_id is not None:
            filters.append(Submittal.product_id == product_id)
        if consultant_id:
            filters.append(Submittal.consultant_id == consultant_id)
        if status:
            filters.append(Submittal.status == status)

        total = self.db.scalar(select(func.count()).select_from(Submittal).where(*filters)) or 0
        rows = self.db.scalars(
            select(Submittal)
            .where(*filters)
            .order_by(Submittal.created_at.desc())
            .offset(pagination.offset)
            .limit(pagination.page_size)
        ).all()
        return SubmittalListResponse(
            total=total, page=pagination.page, page_size=pagination.page_size,
            submittals=[SubmittalListItem.model_validate(s) for s in rows],
        )

    def detail(self, submittal_id: int) -> SubmittalDetail:
        s = self.get_or_404(submittal_id)
        actor_ids = {a.actor_id for a in s.audit_entries}
        names = dict(
            self.db.execute(select(User.id, User.username).where(User.id.in_(actor_ids))).all()
        ) if actor_ids else {}
        detail = SubmittalDetail.model_validate(s)
        detail.audit_trail = [
            AuditEntry(action=a.action, actor=names.get(a.actor_id), timestamp=a.timestamp)
            for a in sorted(s.audit_entries, key=lambda a: a.timestamp)
        ]
        return detail

    def archive(self, submittal_id: int, user_id: int) -> datetime:
        s = self.get_or_404(submittal_id)
        s.status = "archived"
        now = datetime.now(timezone.utc)
        self.db.add(
            SubmittalAudit(submittal_id=s.id, action="archived", actor_id=user_id)
        )
        audit_service.record(
            self.db, user_id=user_id, action="submittal.archived",
            resource_type="submittal", resource_id=s.id,
        )
        self.db.commit()
        return now
