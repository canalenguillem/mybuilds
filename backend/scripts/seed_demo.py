"""Populate the app with realistic demo data for a shareable walkthrough.

Creates products, sample PDF documents (datasheets/certificates/consultant
specs), templates, generated submittals, and AI compliance statements (some
approved and rendered into the PDFs). Idempotent: skips if demo data exists.

Run inside the backend container:
    docker compose exec backend python scripts/seed_demo.py
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy import select

from app.config import settings
from app.database.base import Base
from app.database.session import SessionLocal, engine
import app.database.models  # noqa: F401
from app.database.models.compliance import ComplianceStatement
from app.database.models.products import Product
from app.database.models.users import User
from app.models.products import ProductCreate
from app.models.templates import SectionInput, TemplateCreate
from app.models.submittals import GenerateRequest
from app.services.compliance_service import ComplianceService
from app.services.document_service import DocumentService
from app.services.product_service import ProductService
from app.services.submittal_service import SubmittalService
from app.services.template_service import TemplateService


class _Upload:
    """Minimal stand-in for FastAPI's UploadFile (filename + .file)."""

    def __init__(self, filename: str, data: bytes) -> None:
        self.filename = filename
        self.file = io.BytesIO(data)


def _pdf(title: str, lines: list[str], pages: int = 1) -> bytes:
    out = io.BytesIO()
    c = canvas.Canvas(out, pagesize=A4)
    for pg in range(pages):
        c.setFont("Helvetica-Bold", 16)
        c.drawString(60, 780, title)
        c.setFont("Helvetica", 11)
        y = 740
        for ln in lines:
            c.drawString(60, y, ln)
            y -= 20
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(60, 60, f"Page {pg + 1} of {pages}")
        c.showPage()
    c.save()
    out.seek(0)
    return out.getvalue()


# (product, category, sku, datasheet lines, cert lines, consultant requirement lines)
DATASET = [
    (
        "HVAC Rooftop Unit", "HVAC", "PRD-HVAC-001",
        ["Cooling capacity: 25 kW", "Refrigerant: R-32", "Efficiency: SEER 16",
         "Operating range: -5C to 52C", "Sound level: 58 dB(A)"],
        ["ISO 9001:2015 Quality Management certified", "Tested to EN 14511",
         "CE marked per Machinery Directive"],
        ["The product shall comply with ISO 9001:2015 quality management.",
         "Units must carry CE marking per EN 14511.",
         "Sound level shall not exceed 60 dB(A)."],
    ),
    (
        "Fire-Rated Steel Door", "Doors", "PRD-DOOR-001",
        ["Fire rating: 120 minutes", "Core: mineral wool", "Finish: powder-coated steel",
         "Leaf thickness: 46 mm"],
        ["Certified to BS EN 1634-1", "UL 10C listed", "Intumescent seals included"],
        ["Doors shall provide a minimum 90-minute fire rating.",
         "Materials shall be tested to BS EN 1634-1.",
         "All hardware must be CE marked."],
    ),
    (
        "Cable Tray System", "Electrical", "PRD-CT-001",
        ["Material: hot-dip galvanized steel", "Load class: medium duty",
         "Finish: Z275 coating", "Standard length: 3 m"],
        ["Manufactured to IEC 61537", "RoHS compliant", "ASTM A123 galvanizing"],
        ["Cable trays shall comply with IEC 61537.",
         "Galvanizing shall meet ASTM A123.",
         "Supplier must provide test certificates per batch."],
    ),
]

PROJECTS = [
    ("Downtown Office Complex", "DOC-2026-001", "CONS-001"),
    ("Marina Residential Tower", "MRT-2026-014", "CONS-002"),
    ("Airport Terminal Expansion", "ATE-2026-007", "CONS-003"),
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.scalar(select(Product).where(Product.sku == "PRD-HVAC-001")):
            print("Demo data already present — nothing to do.")
            return

        admin = db.scalar(select(User).where(User.email == settings.seed_admin_email))
        if not admin:
            print("Run scripts/seed_data.py first (admin user missing).", file=sys.stderr)
            sys.exit(1)

        products = ProductService(db)
        docs = DocumentService(db)
        templates = TemplateService(db)
        submittals = SubmittalService(db)

        for i, (name, category, sku, ds_lines, cert_lines, req_lines) in enumerate(DATASET):
            product = products.create(
                ProductCreate(name=name, category=category, sku=sku,
                              description=f"{name} — demo product"),
                admin.id,
            )

            datasheet = docs.upload(
                upload=_Upload("datasheet.pdf", _pdf(f"{name} — Datasheet", ds_lines, pages=3)),
                product_id=product.id, document_type="datasheets",
                title=f"{name} Datasheet", description=None, user=admin,
            )
            cert = docs.upload(
                upload=_Upload("certificate.pdf", _pdf(f"{name} — Certificate", cert_lines, pages=2)),
                product_id=product.id, document_type="certificates",
                title=f"{name} Certificate", description=None, user=admin,
            )
            spec = docs.upload(
                upload=_Upload("spec.pdf", _pdf("Consultant Specification", req_lines, pages=1)),
                product_id=product.id, document_type="compliance_docs",
                title=f"Consultant Spec — {name}", description=None, user=admin,
            )

            template = templates.create(
                TemplateCreate(
                    name=f"{name} Submittal", product_id=product.id,
                    consultant_id=PROJECTS[i][2], template_type="product_generic",
                    branding_config={"primary_color": "#0066cc"},
                    sections=[
                        SectionInput(section_name="Product Datasheet", section_order=1,
                                     section_type="static_document", document_ids=[datasheet.id]),
                        SectionInput(section_name="Certificates", section_order=2,
                                     section_type="static_document", document_ids=[cert.id]),
                        SectionInput(section_name="Compliance Statement", section_order=3,
                                     section_type="dynamic_compliance"),
                    ],
                ),
                admin.id,
            )

            project_name, project_code, consultant = PROJECTS[i]
            submittal = submittals.create_pending(
                GenerateRequest(template_id=template.id, product_id=product.id,
                                consultant_id=consultant, project_name=project_name,
                                project_code=project_code),
                admin,
            )
            submittals.run_generation(submittal.id)

            # AI compliance (stub or OpenAI), then approve and regenerate the PDF.
            ComplianceService(db).run_analysis(
                requirements_doc_id=spec.id, product_ids=[product.id],
                submittal_id=submittal.id,
            )
            stmts = db.scalars(
                select(ComplianceStatement).where(ComplianceStatement.submittal_id == submittal.id)
            ).all()
            # Approve all but the last so the demo shows both approved + pending.
            for s in stmts[:-1]:
                s.review_status = "approved"
                s.reviewer_id = admin.id
                s.reviewed_at = datetime.now(timezone.utc)
            db.commit()
            submittals.run_generation(submittal.id)  # regenerate with approved statements

            print(f"Seeded: {name} (submittal {submittal.submission_number}, "
                  f"{len(stmts)} statements)")

        print("Demo seed complete.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    try:
        seed()
    except Exception as exc:  # pragma: no cover
        print(f"Demo seed failed: {exc}", file=sys.stderr)
        sys.exit(1)
