import sys
from pathlib import Path
import datetime
from unittest.mock import MagicMock

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from services.firestore_subscription_service import (  # type: ignore  # noqa: E402
    FirestoreSubscriptionService,
    SubscriptionRecord,
)


class FakeDocument:
    def __init__(self, data, doc_id="fake-id"):
        self._data = data
        self.id = doc_id
        self.reference = MagicMock()

    def to_dict(self):
        return self._data


class FakeQuery:
    def __init__(self, documents):
        self._documents = documents

    def stream(self):
        for doc in self._documents:
            yield doc

    def where(self, *_args, **_kwargs):
        return self


class FakeCollection:
    def __init__(self, documents):
        self._documents = documents

    def where(self, *_args, **_kwargs):
        return FakeQuery(self._documents)


class FakeClient:
    def __init__(self, documents):
        self._documents = documents

    def collection(self, _name):
        return FakeCollection(self._documents)


def make_record(email="user@example.com", topic="news"):
    return SubscriptionRecord(
        subscription_id="sub-1",
        email=email,
        topic=topic,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        is_active=True,
        last_sent=None,
    )


def test_list_active_subscriptions_returns_records():
    record = make_record()
    client = FakeClient([FakeDocument(record.to_dict())])
    service = FirestoreSubscriptionService("project", client=client)

    records = service.list_active_subscriptions()

    assert len(records) == 1
    assert records[0].email == record.email


def test_update_last_sent_updates_document():
    record = make_record()
    doc = FakeDocument(record.to_dict(), doc_id="sub-1")
    client = FakeClient([doc])
    service = FirestoreSubscriptionService("project", client=client)

    now = datetime.datetime.now(datetime.timezone.utc)
    service.update_last_sent(record.email, record.topic, now)

    doc.reference.update.assert_called_once()
    args, _ = doc.reference.update.call_args
    assert args[0]["last_sent"] == now.isoformat()
