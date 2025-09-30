"""Firestore service for managing topic subscriptions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol, runtime_checkable
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
        self._client = client or firestore.Client(project=project_id)

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


class FirestoreClientError(RuntimeError):
    """Raised when Firestore operations fail."""


