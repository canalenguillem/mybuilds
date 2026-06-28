"""Product business logic: CRUD, listing with counts, documents-by-type."""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.models.documents import Document
from app.database.models.products import Product
from app.database.models.templates import Template
from app.exceptions import ConflictError, NotFoundError
from app.models.common import PaginationParams
from app.models.documents import ProductDocumentBrief, ProductDocumentsResponse
from app.models.products import (
    ProductCreate,
    ProductListItem,
    ProductListResponse,
    ProductUpdate,
)
from app.services import audit_service


class ProductService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_404(self, product_id: int) -> Product:
        product = self.db.get(Product, product_id)
        if not product:
            raise NotFoundError(f"Product {product_id} was not found.")
        return product

    def create(self, data: ProductCreate, user_id: int) -> Product:
        if data.sku and self.db.scalar(select(Product).where(Product.sku == data.sku)):
            raise ConflictError("A product with this SKU already exists.", {"field": "sku"})
        product = Product(**data.model_dump())
        self.db.add(product)
        self.db.flush()
        audit_service.record(
            self.db, user_id=user_id, action="product.created",
            resource_type="product", resource_id=product.id,
        )
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product_id: int, data: ProductUpdate, user_id: int) -> Product:
        product = self.get_or_404(product_id)
        changes = data.model_dump(exclude_unset=True)
        if "sku" in changes and changes["sku"] and changes["sku"] != product.sku:
            if self.db.scalar(select(Product).where(Product.sku == changes["sku"])):
                raise ConflictError("A product with this SKU already exists.", {"field": "sku"})
        for key, value in changes.items():
            setattr(product, key, value)
        audit_service.record(
            self.db, user_id=user_id, action="product.updated",
            resource_type="product", resource_id=product.id, changes=changes,
        )
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product_id: int, user_id: int) -> None:
        product = self.get_or_404(product_id)
        audit_service.record(
            self.db, user_id=user_id, action="product.deleted",
            resource_type="product", resource_id=product.id,
        )
        self.db.delete(product)
        self.db.commit()

    def list(
        self,
        pagination: PaginationParams,
        category: str | None = None,
        is_active: bool | None = None,
        search: str | None = None,
    ) -> ProductListResponse:
        filters = []
        if category:
            filters.append(Product.category == category)
        if is_active is not None:
            filters.append(Product.is_active == is_active)
        if search:
            filters.append(Product.name.like(f"%{search}%"))

        total = self.db.scalar(select(func.count()).select_from(Product).where(*filters)) or 0
        rows = self.db.scalars(
            select(Product)
            .where(*filters)
            .order_by(Product.created_at.desc())
            .offset(pagination.offset)
            .limit(pagination.page_size)
        ).all()

        # Per-product document / template counts.
        items: list[ProductListItem] = []
        for p in rows:
            doc_count = self.db.scalar(
                select(func.count()).select_from(Document).where(Document.product_id == p.id)
            ) or 0
            tpl_count = self.db.scalar(
                select(func.count()).select_from(Template).where(Template.product_id == p.id)
            ) or 0
            items.append(
                ProductListItem(
                    id=p.id, name=p.name, category=p.category, sku=p.sku,
                    is_active=p.is_active, document_count=doc_count, templates_count=tpl_count,
                )
            )

        return ProductListResponse(
            total=total, page=pagination.page, page_size=pagination.page_size, products=items
        )

    def documents_by_type(self, product_id: int) -> ProductDocumentsResponse:
        product = self.get_or_404(product_id)
        docs = self.db.scalars(
            select(Document)
            .where(Document.product_id == product_id, Document.is_current_version.is_(True))
            .order_by(Document.document_type, Document.title)
        ).all()

        grouped: dict[str, list[ProductDocumentBrief]] = {}
        for d in docs:
            grouped.setdefault(d.document_type, []).append(
                ProductDocumentBrief.model_validate(d)
            )

        return ProductDocumentsResponse(
            product_id=product.id, product_name=product.name, documents=grouped
        )
