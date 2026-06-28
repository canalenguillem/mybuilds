"""Aggregates all v1 routers under a single APIRouter."""
from fastapi import APIRouter

from app.api.v1 import auth, documents, health, products

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(products.router)
api_router.include_router(documents.router)

# Future routers (templates, submittals, compliance, analytics) are registered
# here as they are implemented.
