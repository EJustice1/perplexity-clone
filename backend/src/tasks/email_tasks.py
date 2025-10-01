"""Celery tasks for Stage 5 email dispatch."""

from datetime import datetime, timezone

from celery import Celery

from core.app_settings import app_settings
from services.email_sender import EmailSender
from services.summary_generator import SummaryGenerator
from services.firestore_subscription_service import FirestoreSubscriptionService

celery_app = Celery("email_tasks")
celery_app.conf.broker_url = app_settings.celery_broker_url
celery_app.conf.result_backend = app_settings.celery_result_backend


def enqueue_send_email(email: str, topic: str, subscription_id: str) -> None:
    """Queue a Celery task for sending an email."""

    celery_app.send_task(
        "send_subscription_email",
        kwargs={
            "email": email,
            "topic": topic,
            "subscription_id": subscription_id,
        },
    )


@celery_app.task(bind=True, name="send_subscription_email")
def send_subscription_email(self, email: str, topic: str, subscription_id: str) -> None:
    summary_generator = SummaryGenerator()
    firestore_service = FirestoreSubscriptionService(
        project_id=app_settings.gcp_project_id,
        collection_name=app_settings.firestore_collection,
    )
    email_sender = EmailSender(
        host=app_settings.smtp_host,
        port=app_settings.smtp_port,
        username=app_settings.smtp_username,
        password=app_settings.smtp_password,
        use_tls=app_settings.smtp_use_tls,
    )

    summary = summary_generator.generate_summary(topic)
    body = f"Subject: {topic}\n\n{summary}\n\n(placeholder)"
    email_sender.send_plaintext(
        to_email=email,
        subject=f"Weekly Update: {topic}",
        body=body,
        from_email=app_settings.smtp_from,
    )
    firestore_service.update_last_sent(email, topic, datetime.now(timezone.utc))

