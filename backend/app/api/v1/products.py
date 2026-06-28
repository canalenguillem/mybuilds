"""Product management routes."""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.models.users import ROLE_ADMIN, ROLE_OPERATOR, User
from app.database.session import get_db
from app.dependencies import get_current_user, require_roles
from app.models.common import MessageResponse, PaginationParams
from app.models.documents import ProductDocumentsResponse
from app.models.products import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

writer = require_roles(ROLE_ADMIN, ROLE_OPERATOR)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate, db: Session = Depends(get_db), user: User = Depends(writer)
) -> ProductResponse:
    return ProductResponse.model_validate(ProductService(db).create(data, user.id))


@router.get("", response_model=ProductListResponse)
def list_products(
    category: str | None = None,
    is_active: bool | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ProductListResponse:
    pagination = PaginationParams(page=page, page_size=page_size)
    return ProductService(db).list(pagination, category, is_active, search)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> ProductResponse:
    return ProductResponse.model_validate(ProductService(db).get_or_404(product_id))


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(writer),
) -> ProductResponse:
    return ProductResponse.model_validate(ProductService(db).update(product_id, data, user.id))


@router.delete("/{product_id}", response_model=MessageResponse)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(ROLE_ADMIN)),
) -> MessageResponse:
    ProductService(db).delete(product_id, user.id)
    return MessageResponse(message="Product deleted successfully")


@router.get("/{product_id}/documents", response_model=ProductDocumentsResponse)
def product_documents(
    product_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> ProductDocumentsResponse:
    return ProductService(db).documents_by_type(product_id)
