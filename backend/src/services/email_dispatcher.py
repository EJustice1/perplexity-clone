"""Dispatcher helper that enqueues Celery email tasks."""

from typing import Iterable

from services.firestore_subscription_service import SubscriptionRecord
from tasks.email_tasks import enqueue_send_email

class EmailDispatcher:
    """Send subscription records to Celery worker queue."""

    def dispatch(self, subscriptions: Iterable[SubscriptionRecord]) -> int:
        count = 0
        for record in subscriptions:
            enqueue_send_email(record.email, record.topic, record.subscription_id)
            count += 1
        return count

