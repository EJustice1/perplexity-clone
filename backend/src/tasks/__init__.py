"""Celery task package initialization."""

from .email_tasks import celery_app, send_subscription_email

__all__ = ["celery_app", "send_subscription_email"]

