"""PDF assembly: merge section documents, build cover + auto TOC, add page
numbering and branded footers. Pure functions so the Celery task can call them.
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

PAGE_W, PAGE_H = A4
TOC_PER_PAGE = 28
DEFAULT_PRIMARY = "#0066cc"


@dataclass
class SectionSpec:
    name: str
    section_type: str
    doc_paths: list[str] = field(default_factory=list)


@dataclass
class BuildResult:
    page_count: int
    file_size: int
    output_path: str


def _hex(color: str | None) -> HexColor:
    try:
        return HexColor(color or DEFAULT_PRIMARY)
    except (ValueError, TypeError):
        return HexColor(DEFAULT_PRIMARY)


def _cover_page(buf: canvas.Canvas, *, title: str, project_name: str | None,
                consultant_id: str | None, submission_number: str, primary) -> None:
    buf.setFillColor(primary)
    buf.rect(0, PAGE_H - 14 * mm, PAGE_W, 14 * mm, fill=1, stroke=0)
    buf.setFillColor(HexColor("#1a1a1a"))
    buf.setFont("Helvetica-Bold", 28)
    buf.drawString(25 * mm, PAGE_H - 80 * mm, "Technical Submittal")
    buf.setFont("Helvetica", 16)
    buf.setFillColor(HexColor("#374151"))
    buf.drawString(25 * mm, PAGE_H - 92 * mm, title)

    y = PAGE_H - 120 * mm
    buf.setFont("Helvetica", 12)
    for label, value in [
        ("Submission No.", submission_number),
        ("Project", project_name or "—"),
        ("Consultant", consultant_id or "—"),
    ]:
        buf.setFillColor(HexColor("#6b7685"))
        buf.drawString(25 * mm, y, label)
        buf.setFillColor(HexColor("#1a1a1a"))
        buf.drawString(70 * mm, y, str(value))
        y -= 9 * mm
    buf.showPage()


def _toc_pages(buf: canvas.Canvas, entries: list[tuple[str, int]], primary) -> None:
    pages = max(1, math.ceil(len(entries) / TOC_PER_PAGE))
    for p in range(pages):
        buf.setFillColor(primary)
        buf.setFont("Helvetica-Bold", 18)
        buf.drawString(25 * mm, PAGE_H - 30 * mm, "Table of Contents")
        buf.setStrokeColor(HexColor("#e6eaef"))
        buf.line(25 * mm, PAGE_H - 34 * mm, PAGE_W - 25 * mm, PAGE_H - 34 * mm)

        y = PAGE_H - 46 * mm
        chunk = entries[p * TOC_PER_PAGE : (p + 1) * TOC_PER_PAGE]
        buf.setFont("Helvetica", 11)
        for i, (name, page_no) in enumerate(chunk, start=p * TOC_PER_PAGE + 1):
            buf.setFillColor(HexColor("#374151"))
            buf.drawString(25 * mm, y, f"{i}.  {name[:70]}")
            buf.setFillColor(HexColor("#6b7685"))
            buf.drawRightString(PAGE_W - 25 * mm, y, str(page_no))
            y -= 8 * mm
        buf.showPage()


def _placeholder_page(name: str, section_type: str) -> bytes:
    out = BytesIO()
    c = canvas.Canvas(out, pagesize=A4)
    c.setFillColor(HexColor("#1a1a1a"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(25 * mm, PAGE_H - 60 * mm, name)
    c.setFillColor(HexColor("#6b7685"))
    c.setFont("Helvetica", 12)
    note = (
        "Compliance statement to be generated."
        if section_type == "dynamic_compliance"
        else "No documents attached to this section."
    )
    c.drawString(25 * mm, PAGE_H - 72 * mm, note)
    c.showPage()
    c.save()
    out.seek(0)
    return out.getvalue()


def _front_matter(*, title, project_name, consultant_id, submission_number,
                  toc_entries, primary) -> bytes:
    out = BytesIO()
    c = canvas.Canvas(out, pagesize=A4)
    _cover_page(c, title=title, project_name=project_name, consultant_id=consultant_id,
                submission_number=submission_number, primary=primary)
    _toc_pages(c, toc_entries, primary)
    c.save()
    out.seek(0)
    return out.getvalue()


def _footer_overlay(width: float, height: float, *, primary, left: str, right: str) -> PdfReader:
    out = BytesIO()
    c = canvas.Canvas(out, pagesize=(width, height))
    c.setStrokeColor(primary)
    c.setLineWidth(0.6)
    c.line(18 * mm, 12 * mm, width - 18 * mm, 12 * mm)
    c.setFont("Helvetica", 8)
    c.setFillColor(HexColor("#6b7685"))
    c.drawString(18 * mm, 7 * mm, left[:90])
    c.drawRightString(width - 18 * mm, 7 * mm, right)
    c.save()
    out.seek(0)
    return PdfReader(out)


def build_submittal(
    *,
    output_path: str,
    submission_number: str,
    title: str,
    project_name: str | None,
    consultant_id: str | None,
    branding: dict | None,
    sections: list[SectionSpec],
    progress=None,
) -> BuildResult:
    """Assemble the final submittal PDF. ``progress(pct, message)`` is optional."""
    primary = _hex((branding or {}).get("primary_color"))

    def tick(pct, msg):
        if progress:
            progress(pct, msg)

    # 1) Merge section content, recording each section's start page (0-based).
    tick(20, "Merging documents")
    content = PdfWriter()
    starts: list[tuple[str, int]] = []
    for sec in sections:
        starts.append((sec.name, len(content.pages)))
        added = False
        for path in sec.doc_paths:
            if path and os.path.exists(path):
                try:
                    for page in PdfReader(path).pages:
                        content.add_page(page)
                    added = True
                except Exception:  # noqa: BLE001 — skip unreadable PDFs gracefully
                    continue
        if not added:
            for page in PdfReader(BytesIO(_placeholder_page(sec.name, sec.section_type))).pages:
                content.add_page(page)

    # 2) Front matter (cover + TOC) with absolute page numbers.
    tick(55, "Building cover and table of contents")
    toc_page_count = max(1, math.ceil(len(sections) / TOC_PER_PAGE))
    front_count = 1 + toc_page_count
    toc_entries = [(name, front_count + start + 1) for name, start in starts]
    front_bytes = _front_matter(
        title=title, project_name=project_name, consultant_id=consultant_id,
        submission_number=submission_number, toc_entries=toc_entries, primary=primary,
    )

    # 3) Assemble final document: front matter + content.
    final = PdfWriter()
    for page in PdfReader(BytesIO(front_bytes)).pages:
        final.add_page(page)
    content_buf = BytesIO()
    content.write(content_buf)
    content_buf.seek(0)
    for page in PdfReader(content_buf).pages:
        final.add_page(page)

    total = len(final.pages)

    # 4) Branded footer + page numbers on every page.
    tick(80, "Applying page numbers and branding")
    footer_left = f"{submission_number}  ·  {project_name or title}"
    for i, page in enumerate(final.pages, start=1):
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        overlay = _footer_overlay(
            w, h, primary=primary, left=footer_left, right=f"Page {i} of {total}"
        )
        page.merge_page(overlay.pages[0])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as fh:
        final.write(fh)
    tick(95, "Finalizing")

    return BuildResult(page_count=total, file_size=os.path.getsize(output_path), output_path=output_path)
