"""Dispatcher service orchestrating Stage 5 batching."""

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

from .firestore_subscription_service import FirestoreSubscriptionService

@dataclass
class TopicBatch:
    topic: str
    emails: List[str]

class DispatcherService:
    """Service responsible for Stage 5 batching logic."""

    def __init__(self, firestore_service: FirestoreSubscriptionService) -> None:
        self._firestore_service = firestore_service

    def gather_batches(self) -> List[TopicBatch]:
        records = self._firestore_service.list_active_subscriptions()
        grouped: Dict[str, List[str]] = defaultdict(list)
        for record in records:
            grouped[record.topic].append(record.email)
        return [TopicBatch(topic=topic, emails=emails) for topic, emails in grouped.items()]

    def enqueue_batches(self) -> Dict[str, int]:
        batches = self.gather_batches()
        return {batch.topic: len(batch.emails) for batch in batches}
