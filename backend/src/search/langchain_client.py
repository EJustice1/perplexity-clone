"""LangChain client scaffolding for the adaptive search pipeline.

This module defines placeholders for the LangChain components that will be
implemented in later stages. Stage 1 configures dependency loading and
establishes the integration surface for query decomposition, retrieval, and
answer synthesis.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class LangChainConfig:
    """Configuration values required to initialize LangChain components.

    Attributes:
        serp_api_key: API key used for web search connectors.
        gemini_api_key: API key for Gemini models used via LangChain.
    """

    serp_api_key: Optional[str]
    gemini_api_key: Optional[str]


class LangChainClient:
    """Placeholder client for LangChain-based search orchestration.

    Stage 1 does not instantiate LangChain objects. Future stages will extend
    this class to build query decomposition chains, search retrievers, and RAG
    pipelines using the dependencies installed in this phase.
    """

    def __init__(self, config: LangChainConfig) -> None:
        """Store configuration for later initialization.

        Args:
            config: Configuration values required to build LangChain chains.
        """

        self._config = config

    def is_configured(self) -> bool:
        """Return True when both mandatory API keys are present."""

        return bool(self._config.serp_api_key and self._config.gemini_api_key)

    def build_pipeline(self) -> Dict[str, Any]:
        """Return placeholders for pipeline components.

        Future stages will replace this with LangChain chains that perform
        adaptive query decomposition, multi-search retrieval, and answer
        synthesis.
        """

        raise NotImplementedError("LangChain pipeline construction pending")

