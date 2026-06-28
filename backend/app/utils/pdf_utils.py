"""PDF helpers shared across services."""
from __future__ import annotations

import os

from pypdf import PdfReader
from pypdf.errors import PdfReadError


def extract_text(path: str | None, max_pages: int = 40) -> str:
    """Best-effort text extraction from a PDF; returns '' on any failure."""
    if not path or not os.path.exists(path):
        return ""
    try:
        reader = PdfReader(path)
    except (PdfReadError, OSError, ValueError):
        return ""
    parts: list[str] = []
    for page in reader.pages[:max_pages]:
        try:
            parts.append(page.extract_text() or "")
        except Exception:  # noqa: BLE001 — one bad page shouldn't abort the rest
            continue
    return "\n".join(parts).strip()
