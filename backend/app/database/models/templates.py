"""Template, section and template version models."""
from datetime import datetime

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin


class Template(Base, TimestampMixin):
    __tablename__ = "templates"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    product_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("products.id", ondelete="SET NULL"), index=True
    )
    consultant_id: Mapped[str | None] = mapped_column(String(100), index=True)
    template_type: Mapped[str | None] = mapped_column(String(50), index=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    is_current_version: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    branding_config: Mapped[dict | None] = mapped_column(JSON)
    header_footer_config: Mapped[dict | None] = mapped_column(JSON)
    created_by: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)

    sections: Mapped[list["TemplateSection"]] = relationship(
        back_populates="template",
        cascade="all, delete-orphan",
        order_by="TemplateSection.section_order",
    )


class TemplateSection(Base, TimestampMixin):
    __tablename__ = "template_sections"
    __table_args__ = (
        UniqueConstraint("template_id", "section_order", name="unique_section_order"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    template_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("templates.id", ondelete="CASCADE"), nullable=False, index=True
    )
    section_name: Mapped[str] = mapped_column(String(255), nullable=False)
    section_order: Mapped[int] = mapped_column(Integer, nullable=False)
    section_type: Mapped[str | None] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text)
    document_ids: Mapped[list | None] = mapped_column(JSON)
    conditional_logic: Mapped[dict | None] = mapped_column(JSON)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True)
    is_editable: Mapped[bool] = mapped_column(Boolean, default=False)

    template: Mapped["Template"] = relationship(back_populates="sections")


class TemplateVersion(Base):
    __tablename__ = "template_versions"
    __table_args__ = (
        UniqueConstraint("template_id", "version", name="unique_template_version"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    template_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("templates.id", ondelete="CASCADE"), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    version_data: Mapped[dict | None] = mapped_column(JSON)
    created_by: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    change_description: Mapped[str | None] = mapped_column(Text)
