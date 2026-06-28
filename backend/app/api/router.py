"""Aggregates all v1 routers under a single APIRouter."""
from fastapi import APIRouter

from app.api.v1 import (
    auth,
    compliance,
    documents,
    health,
    products,
    submittals,
    templates,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(products.router)
api_router.include_router(documents.router)
api_router.include_router(templates.router)
api_router.include_router(submittals.router)
api_router.include_router(compliance.router)

# Future routers (analytics) are registered here as they are implemented.
