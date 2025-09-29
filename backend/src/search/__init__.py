"""Search orchestration package for LangChain integration.

This package now exposes the adaptive query decomposition client introduced in
Stage 2, while leaving retrieval and synthesis for future stages.
"""

from .langchain_client import LangChainClient, LangChainConfig
from .multi_search import (
    MultiQuerySearchOrchestrator,
    MultiSearchResponse,
    PerQuerySearchOutcome,
)
from .content_collator import (
    ContentCollator,
    ContentCollation,
    CollatedDocument,
    CollationSummary,
)
from .answer_synthesizer import (
    AnswerSynthesizer,
    SynthesizedAnswer,
)

__all__ = [
    "LangChainClient",
    "LangChainConfig",
    "create_decomposition_client",
    "decompose_query",
    "MultiQuerySearchOrchestrator",
    "MultiSearchResponse",
    "PerQuerySearchOutcome",
    "ContentCollator",
    "ContentCollation",
    "CollatedDocument",
    "CollationSummary",
    "AnswerSynthesizer",
    "SynthesizedAnswer",
]


def create_decomposition_client(config: LangChainConfig) -> LangChainClient:
    """Instantiate a LangChain client prepared for query decomposition."""

    return LangChainClient(config)


def decompose_query(
    client: LangChainClient, user_query: str
) -> list[str]:
    """Delegate query decomposition to the provided client instance."""

    return client.decompose_query(user_query)

