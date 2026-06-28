"""LLM integration for compliance analysis (OpenAI), with a no-key fallback.

When OPENAI_API_KEY is set, calls the OpenAI Chat Completions API with JSON mode.
When it's absent, returns deterministic stub output so the feature is fully
demonstrable without spending credits — clearly flagged via ``ai_model``.
"""
from __future__ import annotations

import json
import re

from app.config import settings

# Cap text sent to the model to keep token usage (and cost) bounded.
_MAX_CHARS = 12000

_EXTRACT_SYSTEM = (
    "You are a compliance engineer for a UAE building-materials supplier. "
    "Extract discrete, checkable technical requirements from a consultant's "
    "specification document. Return JSON only."
)

_STATEMENT_SYSTEM = (
    "You are a compliance engineer. For each requirement, draft a concise, "
    "professional compliance statement describing how the product complies, "
    "grounded ONLY in the supplied product documentation. If the documents do "
    "not support compliance, say so and lower the confidence. Return JSON only."
)


class AIService:
    def __init__(self) -> None:
        self.model = settings.openai_model
        self._client = None
        if settings.openai_api_key:
            from openai import OpenAI

            self._client = OpenAI(
                api_key=settings.openai_api_key, timeout=settings.openai_timeout
            )

    @property
    def model_label(self) -> str:
        return self.model if self._client else "stub"

    @property
    def enabled(self) -> bool:
        return self._client is not None

    # ── Public API ──────────────────────────────────────────────
    def extract_requirements(self, document_text: str) -> list[dict]:
        """Return [{requirement_text, requirement_category, confidence}]."""
        if not self._client:
            return self._stub_requirements(document_text)

        prompt = (
            "Extract the technical/compliance requirements from this document. "
            'Respond as JSON: {"requirements": [{"requirement_text": str, '
            '"requirement_category": str, "confidence": number 0-1}]}.\n\n'
            f"DOCUMENT:\n{document_text[:_MAX_CHARS]}"
        )
        data = self._chat_json(_EXTRACT_SYSTEM, prompt)
        return data.get("requirements", []) if isinstance(data, dict) else []

    def draft_statements(
        self, requirements: list[dict], product_name: str, product_text: str
    ) -> list[dict]:
        """Return [{requirement_index, statement, confidence_score}]."""
        if not self._client:
            return self._stub_statements(requirements, product_name)

        reqs = [
            {"index": i, "requirement_text": r.get("requirement_text", "")}
            for i, r in enumerate(requirements)
        ]
        prompt = (
            f"Product: {product_name}\n"
            f"Product documentation:\n{product_text[:_MAX_CHARS]}\n\n"
            f"Requirements:\n{json.dumps(reqs)}\n\n"
            'Respond as JSON: {"statements": [{"requirement_index": int, '
            '"statement": str, "confidence_score": number 0-1}]}.'
        )
        data = self._chat_json(_STATEMENT_SYSTEM, prompt)
        return data.get("statements", []) if isinstance(data, dict) else []

    # ── OpenAI call ─────────────────────────────────────────────
    def _chat_json(self, system: str, user: str) -> dict:
        resp = self._client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        try:
            return json.loads(resp.choices[0].message.content or "{}")
        except (json.JSONDecodeError, TypeError):
            return {}

    # ── Deterministic fallback (no API key) ─────────────────────
    @staticmethod
    def _stub_requirements(document_text: str) -> list[dict]:
        # Heuristic: lines that look like requirements ("shall", "must", standards).
        lines = [ln.strip(" -•\t") for ln in document_text.splitlines()]
        picked = [
            ln for ln in lines
            if len(ln) > 15
            and re.search(r"\b(shall|must|comply|complies|ISO|EN|ASTM|BS|require)\b", ln, re.I)
        ]
        if not picked:
            picked = [ln for ln in lines if len(ln) > 25][:5]
        out = []
        for ln in picked[:10]:
            category = "quality_management" if re.search(r"ISO", ln) else "general"
            out.append(
                {"requirement_text": ln[:500], "requirement_category": category, "confidence": 0.6}
            )
        return out

    @staticmethod
    def _stub_statements(requirements: list[dict], product_name: str) -> list[dict]:
        out = []
        for i, r in enumerate(requirements):
            text = r.get("requirement_text", "the requirement")
            out.append(
                {
                    "requirement_index": i,
                    "statement": (
                        f"{product_name} complies with: \"{text[:160]}\". "
                        "Supporting documentation (datasheets/certificates) is included "
                        "in this submittal. [Draft generated without LLM — pending review.]"
                    ),
                    "confidence_score": 0.55,
                }
            )
        return out
