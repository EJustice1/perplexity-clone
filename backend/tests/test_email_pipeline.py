import sys
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from services.dispatcher_service import DispatcherService  # type: ignore  # noqa: E402
from services.firestore_subscription_service import SubscriptionRecord  # type: ignore  # noqa: E402
from services.email_dispatcher import EmailDispatcher  # type: ignore  # noqa: E402
from tasks.email_tasks import send_subscription_email  # type: ignore  # noqa: E402

class FakeFirestoreService:
    def __init__(self, records=None):
        self._records = records or []
        self.updated = []

    def list_active_subscriptions(self):
        return self._records

    def update_last_sent(self, email: str, topic: str, when):
        self.updated.append((email, topic, when))

def make_record(email="user@example.com", topic="news"):
    return SubscriptionRecord(
        subscription_id="sub-1",
        email=email,
        topic=topic,
        created_at=datetime.now(timezone.utc),
        is_active=True,
        last_sent=None,
    )

@patch("services.email_dispatcher.enqueue_send_email")
def test_dispatcher_enqueues_celery_tasks(mock_enqueue):
    record = make_record()
    service = DispatcherService(FakeFirestoreService([record]))
    subscriptions = service.gather_subscriptions()
    dispatcher = EmailDispatcher()
    dispatcher.dispatch(subscriptions)
    mock_enqueue.assert_called_once_with(record.email, record.topic, record.subscription_id)

def test_send_subscription_email_updates_firestore():
    record = make_record()
    firestore = FakeFirestoreService()
    with patch("tasks.email_tasks.FirestoreSubscriptionService", return_value=firestore), \
         patch("tasks.email_tasks.EmailSender") as mock_sender:
        send_subscription_email(record.email, record.topic, record.subscription_id)
        mock_sender.return_value.send_plaintext.assert_called_once()
        assert len(firestore.updated) == 1
