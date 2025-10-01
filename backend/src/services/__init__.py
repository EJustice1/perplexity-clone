"""Services module for business logic and external integrations.

Service implementations handle web search, content extraction, LLM synthesis,
and supporting utilities. LangChain integrations are staged into the
`search` package to keep responsibilities clearly separated.
"""

from .firestore_subscription_service import FirestoreSubscriptionService, SubscriptionRecord
from .dispatcher_service import DispatcherService
from .email_sender import EmailSender
from .summary_generator import SummaryGenerator
