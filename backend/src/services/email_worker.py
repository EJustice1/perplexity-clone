from datetime import datetime, timezone
from typing import Protocol

from .email_sender import EmailSender
from .firestore_subscription_service import FirestoreSubscriptionService

class SummaryGeneratorProtocol(Protocol):
    def generate_summary(self, topic: str) -> str:
        ...

class EmailWorker:
    def __init__(
        self,
        email_sender: EmailSender,
        firestore_service: FirestoreSubscriptionService,
        summary_generator: SummaryGeneratorProtocol,
        sender_email: str,
    ) -> None:
        self._email_sender = email_sender
        self._firestore_service = firestore_service
        self._summary_generator = summary_generator
        self._sender_email = sender_email

    def send_subscription_email(self, email: str, topic: str, subscription_id: str) -> None:
        summary = self._summary_generator.generate_summary(topic)
        body = f"Subject: {topic}\n\n{summary}\n\n(placeholder)"
        self._email_sender.send_plaintext(
            to_email=email,
            subject=f"Weekly Update: {topic}",
            body=body,
            from_email=self._sender_email,
        )
        self._firestore_service.update_last_sent(email, topic, datetime.now(timezone.utc))
