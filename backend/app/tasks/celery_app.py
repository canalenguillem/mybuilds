"""Celery application instance.

Tasks (PDF generation, AI compliance analysis, email delivery) will register
against this app in later phases. Defined now so the worker container starts.
"""
from celery import Celery

from app.config import settings

celery_app = Celery(
    "mybuilds",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks.pdf_generation"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)


@celery_app.task(name="health.ping")
def ping() -> str:
    """Trivial task to confirm the worker is wired up."""
    return "pong"
