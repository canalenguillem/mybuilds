"""Compliance analysis orchestration and review."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.models.compliance import (
    ComplianceAnalysisHistory,
    ComplianceRequirement,
    ComplianceStatement,
)
from app.database.models.documents import Document
from app.database.models.products import Product
from app.database.models.users import User
from app.exceptions import NotFoundError
from app.models.common import PaginationParams
from app.models.compliance import (
    ReviewRequest,
    ReviewResponse,
    StatementListItem,
    StatementListResponse,
)
from app.models.common import UserBrief
from app.services import audit_service, settings_service
from app.services.ai_service import AIService
from app.utils.pdf_utils import extract_text

# Product document types that substantiate compliance.
_EVIDENCE_TYPES = ("datasheets", "certificates", "manuals", "compliance_docs")


class ComplianceService:
    def __init__(self, db: Session) -> None:
        self.db = db
        api_key, model = settings_service.get_openai_config(db)
        self.ai = AIService(api_key=api_key, model=model)

    # ── Analysis (invoked by the Celery worker) ─────────────────
    def run_analysis(
        self,
        *,
        requirements_doc_id: int,
        product_ids: list[int],
        submittal_id: int | None,
        progress=None,
    ) -> dict:
        def tick(pct, msg):
            if progress:
                progress(pct, msg)

        doc = self.db.get(Document, requirements_doc_id)
        if not doc:
            raise NotFoundError(f"Requirements document {requirements_doc_id} not found.")

        tick(15, "Reading requirements document")
        requirements = self.ai.extract_requirements(extract_text(doc.file_path))

        tick(40, "Storing extracted requirements")
        req_rows: list[ComplianceRequirement] = []
        for r in requirements:
            row = ComplianceRequirement(
                source_document_id=doc.id,
                source_document_name=doc.title,
                requirement_text=r.get("requirement_text", "")[:2000],
                requirement_category=r.get("requirement_category"),
                ai_extraction_confidence=_clamp(r.get("confidence")),
            )
            self.db.add(row)
            req_rows.append(row)
        self.db.flush()

        tick(55, "Drafting compliance statements")
        statements_made = 0
        step = max(1, len(product_ids))
        for idx, product_id in enumerate(product_ids):
            product = self.db.get(Product, product_id)
            if not product:
                continue
            evidence = self.db.scalars(
                select(Document).where(
                    Document.product_id == product_id,
                    Document.document_type.in_(_EVIDENCE_TYPES),
                    Document.is_current_version.is_(True),
                )
            ).all()
            product_text = "\n\n".join(extract_text(d.file_path) for d in evidence)
            doc_ids = [d.id for d in evidence]

            drafts = self.ai.draft_statements(requirements, product.name, product_text)
            for s in drafts:
                ri = s.get("requirement_index")
                req_row = req_rows[ri] if isinstance(ri, int) and 0 <= ri < len(req_rows) else None
                self.db.add(
                    ComplianceStatement(
                        submittal_id=submittal_id,
                        requirement_id=req_row.id if req_row else None,
                        statement=s.get("statement", "")[:4000],
                        confidence_score=_clamp(s.get("confidence_score")),
                        source_document_ids=doc_ids,
                        is_ai_generated=self.ai.enabled,
                        review_status="pending_review",
                    )
                )
                statements_made += 1
            tick(55 + int(35 * (idx + 1) / step), f"Analyzed product {product.name}")

        self.db.add(
            ComplianceAnalysisHistory(
                submittal_id=submittal_id,
                consultant_requirements_doc_id=doc.id,
                analysis_type="auto_generation",
                analysis_result={
                    "requirements_found": len(req_rows),
                    "statements_generated": statements_made,
                },
                ai_model_used=self.ai.model_label,
            )
        )
        self.db.commit()
        return {
            "requirements_found": len(req_rows),
            "statements_generated": statements_made,
            "ai_model": self.ai.model_label,
        }

    # ── Queries / review ────────────────────────────────────────
    def list_statements(
        self,
        pagination: PaginationParams,
        submittal_id: int | None = None,
        review_status: str | None = None,
        confidence_score_min: float | None = None,
    ) -> StatementListResponse:
        filters = []
        if submittal_id is not None:
            filters.append(ComplianceStatement.submittal_id == submittal_id)
        if review_status:
            filters.append(ComplianceStatement.review_status == review_status)
        if confidence_score_min is not None:
            filters.append(ComplianceStatement.confidence_score >= confidence_score_min)

        total = self.db.scalar(
            select(func.count()).select_from(ComplianceStatement).where(*filters)
        ) or 0
        rows = self.db.scalars(
            select(ComplianceStatement)
            .where(*filters)
            .order_by(ComplianceStatement.created_at.desc())
            .offset(pagination.offset)
            .limit(pagination.page_size)
        ).all()
        return StatementListResponse(
            total=total, page=pagination.page, page_size=pagination.page_size,
            statements=[StatementListItem.model_validate(s) for s in rows],
        )

    def review(self, statement_id: int, data: ReviewRequest, user: User) -> ReviewResponse:
        stmt = self.db.get(ComplianceStatement, statement_id)
        if not stmt:
            raise NotFoundError(f"Compliance statement {statement_id} not found.")
        if data.revised_statement:
            stmt.statement = data.revised_statement
        stmt.review_status = data.review_status
        stmt.reviewer_id = user.id
        stmt.review_notes = data.review_notes
        stmt.reviewed_at = datetime.now(timezone.utc)
        audit_service.record(
            self.db, user_id=user.id, action=f"compliance.{data.review_status}",
            resource_type="compliance_statement", resource_id=stmt.id,
        )
        self.db.commit()
        self.db.refresh(stmt)
        return ReviewResponse(
            id=stmt.id, review_status=stmt.review_status,
            reviewed_by=UserBrief(id=user.id, username=user.username),
            reviewed_at=stmt.reviewed_at, review_notes=stmt.review_notes,
        )

    def get_requirement(self, requirement_id: int) -> ComplianceRequirement:
        req = self.db.get(ComplianceRequirement, requirement_id)
        if not req:
            raise NotFoundError(f"Requirement {requirement_id} not found.")
        return req


def _clamp(value) -> float | None:
    try:
        return max(0.0, min(1.0, round(float(value), 2)))
    except (TypeError, ValueError):
        return None
