"""Firestore service for managing topic subscriptions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol, runtime_checkable, Iterable
import uuid

from google.cloud import firestore
from google.cloud.exceptions import GoogleCloudError


@runtime_checkable
class FirestoreClientProtocol(Protocol):
    """Protocol describing the Firestore client interactions used."""

    def collection(self, collection_name: str):  # pragma: no cover - interface
        ...


@dataclass
class SubscriptionRecord:
    """Data structure representing a stored subscription."""

    subscription_id: str
    email: str
    topic: str
    created_at: datetime
    is_active: bool
    last_sent: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "subscription_id": self.subscription_id,
            "email": self.email,
            "topic": self.topic,
            "created_at": self.created_at,
            "is_active": self.is_active,
            "last_sent": self.last_sent,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "SubscriptionRecord":
        created = data.get("created_at")
        if isinstance(created, datetime):
            created_at = created
        elif created:
            created_at = datetime.fromisoformat(str(created))
        else:
            created_at = datetime.now(timezone.utc)
        return cls(
            subscription_id=str(data.get("subscription_id") or uuid.uuid4().hex),
            email=str(data.get("email")),
            topic=str(data.get("topic")),
            created_at=created_at,
            is_active=bool(data.get("is_active", True)),
            last_sent=data.get("last_sent"),
        )


class FirestoreSubscriptionService:
    """Service providing Firestore persistence for topic subscriptions."""

    def __init__(
        self,
        project_id: str,
        collection_name: str = "topic_subscriptions",
        client: FirestoreClientProtocol | None = None,
    ) -> None:
        self._project_id = project_id
        self._collection_name = collection_name
        if client is not None:
            self._client = client
        else:
            if project_id:
                self._client = firestore.Client(project=project_id)
            else:
                self._client = firestore.Client()

    def create_subscription(self, email: str, topic: str) -> SubscriptionRecord:
        """Persist a new subscription and return the stored record."""

        subscription_id = uuid.uuid4().hex
        now = datetime.now(timezone.utc)
        record = SubscriptionRecord(
            subscription_id=subscription_id,
            email=email,
            topic=topic,
            created_at=now,
            is_active=True,
            last_sent=None,
        )
        try:
            collection = self._client.collection(self._collection_name)
            collection.document(subscription_id).set(record.to_dict())
        except GoogleCloudError as exc:
            raise FirestoreClientError("Failed to persist subscription") from exc

        return record

    def list_active_subscriptions(self) -> list[SubscriptionRecord]:
        """Return all active subscription records."""

        try:
            query = (
                self._client.collection(self._collection_name)
                .where("is_active", "==", True)
            )
            documents: Iterable = query.stream()
        except GoogleCloudError as exc:
            raise FirestoreClientError("Failed to load subscriptions") from exc

        records: list[SubscriptionRecord] = []
        for doc in documents:
            data = doc.to_dict() or {}
            data.setdefault("subscription_id", doc.id)
            records.append(SubscriptionRecord.from_dict(data))
        return records

    def update_last_sent(self, email: str, topic: str, when: datetime) -> None:
        try:
            query = (
                self._client.collection(self._collection_name)
                .where("email", "==", email)
                .where("topic", "==", topic)
            )
            for doc in query.stream():
                doc.reference.update({"last_sent": when.isoformat()})
        except GoogleCloudError as exc:
            raise FirestoreClientError("Failed to update last_sent") from exc


class FirestoreClientError(RuntimeError):
    """Raised when Firestore operations fail."""


