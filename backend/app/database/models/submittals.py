"""Submittal and submittal audit models."""
from datetime import datetime

from sqlalchemy import (
    JSON,
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

SUBMITTAL_STATUSES = ("draft", "generating", "generated", "reviewed", "approved", "archived", "failed")


class Submittal(Base, TimestampMixin):
    __tablename__ = "submittals"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    submission_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("products.id"), nullable=False, index=True
    )
    template_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("templates.id"), nullable=False, index=True
    )
    consultant_id: Mapped[str | None] = mapped_column(String(100), index=True)
    project_name: Mapped[str | None] = mapped_column(String(255))
    project_code: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50), default="draft", index=True)
    generated_file_path: Mapped[str | None] = mapped_column(String(500))
    file_size: Mapped[int | None] = mapped_column(BigInteger)
    page_count: Mapped[int | None] = mapped_column(Integer)
    total_sections: Mapped[int | None] = mapped_column(Integer)
    submittal_metadata: Mapped[dict | None] = mapped_column("metadata", JSON)
    created_by: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False, index=True
    )
    generated_at: Mapped[datetime | None] = mapped_column(DateTime)

    audit_entries: Mapped[list["SubmittalAudit"]] = relationship(
        back_populates="submittal", cascade="all, delete-orphan"
    )


class SubmittalAudit(Base):
    __tablename__ = "submittal_audit"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    submittal_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("submittals.id", ondelete="CASCADE"), nullable=False, index=True
    )
    action: Mapped[str | None] = mapped_column(String(50), index=True)
    actor_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    action_details: Mapped[dict | None] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)

    submittal: Mapped["Submittal"] = relationship(back_populates="audit_entries")
