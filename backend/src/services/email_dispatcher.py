"""Dispatcher helper that enqueues Celery email tasks."""

from typing import Iterable

try:
    from .firestore_subscription_service import SubscriptionRecord
except ImportError:  # Fallback when imported as top-level package
    from services.firestore_subscription_service import SubscriptionRecord

try:
    from ..tasks.email_tasks import enqueue_send_email
except ImportError:  # Fallback when imported as top-level package
    from tasks.email_tasks import enqueue_send_email

class EmailDispatcher:
    """Send subscription records to Celery worker queue."""

    def dispatch(self, subscriptions: Iterable[SubscriptionRecord]) -> int:
        count = 0
        for record in subscriptions:
            enqueue_send_email(record.email, record.topic, record.subscription_id)
            count += 1
        return count

