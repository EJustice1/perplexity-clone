from typing import Dict, List
from datetime import datetime, timezone

from .email_sender import EmailSender
from .firestore_subscription_service import FirestoreSubscriptionService

FIXED_SUBJECT = "Weekly Digest Test"
FIXED_BODY = "Hello! This is your weekly test email from the Perplexity Clone pipeline."

class EmailDispatcher:
    def __init__(self, email_sender: EmailSender, firestore_service: FirestoreSubscriptionService, sender_email: str) -> None:
        self._email_sender = email_sender
        self._firestore_service = firestore_service
        self._sender_email = sender_email

    def dispatch(self, topic_batches: Dict[str, List[str]]) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for topic, emails in topic_batches.items():
            for email in emails:
                self._email_sender.send_plaintext(
                    to_email=email,
                    subject=FIXED_SUBJECT,
                    body=FIXED_BODY,
                    from_email=self._sender_email,
                )
                self._firestore_service.update_last_sent(email, topic, datetime.now(timezone.utc))
            counts[topic] = len(emails)
        return counts
