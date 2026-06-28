"""FastAPI application entry point."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.config import settings
from app.exceptions import AppException
from app.models.responses import ErrorDetail, ErrorResponse

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger("mybuilds")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # In development we create tables on startup so the stack runs without a
    # manual Alembic step. Production uses `alembic upgrade head`.
    if settings.environment == "development":
        from app.database.base import Base
        from app.database.session import engine
        import app.database.models  # noqa: F401  (registers all models)

        Base.metadata.create_all(bind=engine)
        logger.info("Database tables ensured (development mode).")
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=ErrorDetail(code=exc.code, message=exc.message, details=exc.details)
        ).model_dump(mode="json"),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error=ErrorDetail(
                code="INVALID_INPUT",
                message="Request validation failed.",
                details={"errors": exc.errors()},
            )
        ).model_dump(mode="json"),
    )


app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root() -> dict:
    return {"app": settings.app_name, "docs": "/docs", "api": settings.api_v1_prefix}
