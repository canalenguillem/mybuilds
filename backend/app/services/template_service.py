"""Template business logic: CRUD, sections, reorder, versioning."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.models.documents import Document
from app.database.models.templates import (
    Template,
    TemplateSection,
    TemplateVersion,
)
from app.exceptions import BadRequestError, NotFoundError
from app.models.common import PaginationParams
from app.models.templates import (
    ReorderRequest,
    ReorderResponse,
    ReorderedSection,
    SectionDetail,
    SectionInput,
    TemplateCreate,
    TemplateDetail,
    TemplateListItem,
    TemplateListResponse,
    TemplateUpdate,
)


class TemplateService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_404(self, template_id: int) -> Template:
        tpl = self.db.get(Template, template_id)
        if not tpl:
            raise NotFoundError(f"Template {template_id} was not found.")
        return tpl

    # ── Create ──────────────────────────────────────────────────
    def create(self, data: TemplateCreate, user_id: int) -> Template:
        self._validate_sections(data.sections)
        tpl = Template(
            name=data.name,
            description=data.description,
            product_id=data.product_id,
            consultant_id=data.consultant_id,
            template_type=data.template_type,
            branding_config=data.branding_config,
            header_footer_config=data.header_footer_config,
            version=1,
            is_current_version=True,
            is_active=True,
            created_by=user_id,
        )
        for s in data.sections:
            tpl.sections.append(self._build_section(s))
        self.db.add(tpl)
        self.db.flush()
        self._snapshot(tpl, user_id, "Initial version")
        self.db.commit()
        self.db.refresh(tpl)
        return tpl

    # ── Update (full replace, version bump) ─────────────────────
    def update(self, template_id: int, data: TemplateUpdate, user_id: int) -> Template:
        tpl = self.get_or_404(template_id)
        self._validate_sections(data.sections)

        tpl.name = data.name
        tpl.description = data.description
        tpl.product_id = data.product_id
        tpl.consultant_id = data.consultant_id
        tpl.template_type = data.template_type
        tpl.branding_config = data.branding_config
        tpl.header_footer_config = data.header_footer_config
        tpl.version += 1

        # Replace sections wholesale.
        tpl.sections.clear()
        self.db.flush()
        for s in data.sections:
            tpl.sections.append(self._build_section(s))

        self.db.flush()
        self._snapshot(tpl, user_id, f"Version {tpl.version}")
        self.db.commit()
        self.db.refresh(tpl)
        return tpl

    def delete(self, template_id: int) -> None:
        tpl = self.get_or_404(template_id)
        self.db.delete(tpl)
        self.db.commit()

    # ── Reorder (drag-drop) ─────────────────────────────────────
    def reorder(self, template_id: int, data: ReorderRequest, user_id: int) -> ReorderResponse:
        tpl = self.get_or_404(template_id)
        by_id = {s.id: s for s in tpl.sections}

        requested_ids = {item.section_id for item in data.sections}
        if requested_ids - by_id.keys():
            raise BadRequestError(
                "One or more section_id values do not belong to this template.",
                {"invalid": sorted(requested_ids - by_id.keys())},
            )
        new_orders = [item.new_order for item in data.sections]
        if len(set(new_orders)) != len(new_orders):
            raise BadRequestError("new_order values must be unique.", {"field": "sections"})

        # Two-phase write to avoid tripping the unique(template_id, section_order)
        # constraint while values are in flux.
        for s in tpl.sections:
            s.section_order = -(s.id)
        self.db.flush()
        for item in data.sections:
            by_id[item.section_id].section_order = item.new_order
        self.db.flush()
        self.db.commit()

        ordered = sorted(
            (by_id[i.section_id] for i in data.sections), key=lambda s: s.section_order
        )
        return ReorderResponse(
            message="Sections reordered successfully",
            template_id=tpl.id,
            sections=[
                ReorderedSection(
                    section_id=s.id, section_name=s.section_name, new_order=s.section_order
                )
                for s in ordered
            ],
        )

    # ── Read ────────────────────────────────────────────────────
    def list(
        self,
        pagination: PaginationParams,
        product_id: int | None = None,
        consultant_id: str | None = None,
        is_active: bool | None = None,
    ) -> TemplateListResponse:
        filters = []
        if product_id is not None:
            filters.append(Template.product_id == product_id)
        if consultant_id:
            filters.append(Template.consultant_id == consultant_id)
        if is_active is not None:
            filters.append(Template.is_active == is_active)

        total = self.db.scalar(select(func.count()).select_from(Template).where(*filters)) or 0
        rows = self.db.scalars(
            select(Template)
            .where(*filters)
            .order_by(Template.updated_at.desc())
            .offset(pagination.offset)
            .limit(pagination.page_size)
        ).all()

        items = [
            TemplateListItem(
                id=t.id, name=t.name, product_id=t.product_id, consultant_id=t.consultant_id,
                template_type=t.template_type, version=t.version, section_count=len(t.sections),
                is_active=t.is_active, last_updated=t.updated_at,
            )
            for t in rows
        ]
        return TemplateListResponse(
            total=total, page=pagination.page, page_size=pagination.page_size, templates=items
        )

    def detail(self, template_id: int) -> TemplateDetail:
        tpl = self.get_or_404(template_id)
        # Resolve referenced documents once.
        all_ids = {did for s in tpl.sections for did in (s.document_ids or [])}
        docs = (
            {d.id: d for d in self.db.scalars(select(Document).where(Document.id.in_(all_ids)))}
            if all_ids
            else {}
        )
        sections = [
            SectionDetail(
                id=s.id, section_name=s.section_name, section_order=s.section_order,
                section_type=s.section_type, description=s.description,
                document_ids=s.document_ids or [], is_mandatory=s.is_mandatory,
                is_editable=s.is_editable,
                documents=[
                    {"id": docs[d].id, "title": docs[d].title, "file_size": docs[d].file_size}
                    for d in (s.document_ids or [])
                    if d in docs
                ],
            )
            for s in sorted(tpl.sections, key=lambda s: s.section_order)
        ]
        return TemplateDetail(
            id=tpl.id, name=tpl.name, description=tpl.description, product_id=tpl.product_id,
            consultant_id=tpl.consultant_id, template_type=tpl.template_type, version=tpl.version,
            is_active=tpl.is_active, branding_config=tpl.branding_config,
            header_footer_config=tpl.header_footer_config, created_at=tpl.created_at,
            updated_at=tpl.updated_at, sections=sections,
        )

    # ── Helpers ─────────────────────────────────────────────────
    @staticmethod
    def _validate_sections(sections: list[SectionInput]) -> None:
        orders = [s.section_order for s in sections]
        if len(set(orders)) != len(orders):
            raise BadRequestError(
                "section_order values must be unique within a template.",
                {"field": "sections"},
            )

    @staticmethod
    def _build_section(s: SectionInput) -> TemplateSection:
        return TemplateSection(
            section_name=s.section_name,
            section_order=s.section_order,
            section_type=s.section_type,
            description=s.description,
            document_ids=s.document_ids,
            is_mandatory=s.is_mandatory,
            is_editable=s.is_editable,
        )

    def _snapshot(self, tpl: Template, user_id: int, note: str) -> None:
        """Store a full JSON snapshot of the template into template_versions."""
        version_data = {
            "name": tpl.name,
            "description": tpl.description,
            "product_id": tpl.product_id,
            "consultant_id": tpl.consultant_id,
            "template_type": tpl.template_type,
            "branding_config": tpl.branding_config,
            "header_footer_config": tpl.header_footer_config,
            "sections": [
                {
                    "section_name": s.section_name,
                    "section_order": s.section_order,
                    "section_type": s.section_type,
                    "document_ids": s.document_ids,
                    "is_mandatory": s.is_mandatory,
                }
                for s in sorted(tpl.sections, key=lambda s: s.section_order)
            ],
            "snapshot_at": datetime.now(timezone.utc).isoformat(),
        }
        self.db.add(
            TemplateVersion(
                template_id=tpl.id, version=tpl.version, version_data=version_data,
                created_by=user_id, change_description=note,
            )
        )
