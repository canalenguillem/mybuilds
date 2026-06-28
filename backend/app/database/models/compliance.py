"""Compliance statement, requirement and analysis history models."""
from datetime import datetime

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class ComplianceStatement(Base, TimestampMixin):
    __tablename__ = "compliance_statements"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    submittal_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("submittals.id", ondelete="CASCADE"), index=True
    )
    requirement_id: Mapped[int | None] = mapped_column(BigInteger)
    statement: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_score: Mapped[float | None] = mapped_column(Numeric(3, 2), index=True)
    source_document_ids: Mapped[list | None] = mapped_column(JSON)
    is_ai_generated: Mapped[bool] = mapped_column(Boolean, default=True)
    review_status: Mapped[str] = mapped_column(String(50), default="pending_review", index=True)
    reviewer_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.id"))
    review_notes: Mapped[str | None] = mapped_column(Text)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime)


class ComplianceRequirement(Base):
    __tablename__ = "compliance_requirements"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    source_document_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("documents.id", ondelete="SET NULL"), index=True
    )
    source_document_name: Mapped[str | None] = mapped_column(String(255))
    requirement_text: Mapped[str] = mapped_column(Text, nullable=False)
    requirement_category: Mapped[str | None] = mapped_column(String(100), index=True)
    extracted_keywords: Mapped[list | None] = mapped_column(JSON)
    ai_extraction_confidence: Mapped[float | None] = mapped_column(Numeric(3, 2))
    extracted_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class ComplianceAnalysisHistory(Base):
    __tablename__ = "compliance_analysis_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    submittal_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("submittals.id", ondelete="CASCADE"), index=True
    )
    consultant_requirements_doc_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("documents.id")
    )
    analysis_type: Mapped[str | None] = mapped_column(String(50))
    analysis_result: Mapped[dict | None] = mapped_column(JSON)
    ai_model_used: Mapped[str | None] = mapped_column(String(100))
    processing_time_ms: Mapped[int | None] = mapped_column(Integer)
    tokens_used: Mapped[int | None] = mapped_column(Integer)
    cost: Mapped[float | None] = mapped_column(Numeric(8, 4))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
