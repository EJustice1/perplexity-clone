"""Dispatcher service orchestrating Stage 5 queue fan-out."""

from typing import List

from .firestore_subscription_service import FirestoreSubscriptionService, SubscriptionRecord

class DispatcherService:
    """Service responsible for fetching subscriptions for worker fan-out."""

    def __init__(self, firestore_service: FirestoreSubscriptionService) -> None:
        self._firestore_service = firestore_service

    def gather_subscriptions(self) -> List[SubscriptionRecord]:
        return self._firestore_service.list_active_subscriptions()
