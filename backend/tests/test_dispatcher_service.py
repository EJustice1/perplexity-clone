import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from services.dispatcher_service import DispatcherService, TopicBatch  # type: ignore  # noqa: E402
from services.firestore_subscription_service import SubscriptionRecord  # type: ignore  # noqa: E402


class FakeFirestoreService:
    def __init__(self, records):
        self._records = records

    def list_active_subscriptions(self):
        return self._records

def make_record(email, topic):
    return SubscriptionRecord(
        subscription_id=f"id-{email}",
        email=email,
        topic=topic,
        created_at=datetime.now(timezone.utc),
        is_active=True,
        last_sent=None,
    )


def test_gather_batches_groups_by_topic():
    records = [
        make_record("a@example.com", "news"),
        make_record("b@example.com", "news"),
        make_record("c@example.com", "sports"),
    ]
    service = DispatcherService(FakeFirestoreService(records))
    batches = service.gather_batches()
    assert TopicBatch(topic="news", emails=["a@example.com", "b@example.com"]) in batches
    assert TopicBatch(topic="sports", emails=["c@example.com"]) in batches


def test_enqueue_batches_returns_counts():
    records = [
        make_record("a@example.com", "news"),
        make_record("b@example.com", "news"),
        make_record("c@example.com", "sports"),
    ]
    service = DispatcherService(FakeFirestoreService(records))
    counts = service.enqueue_batches()
    assert counts == {"news": 2, "sports": 1}
