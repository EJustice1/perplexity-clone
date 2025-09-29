"""Search orchestration package for LangChain integration.

This package will house the LangChain-powered search pipeline. Stage 1 only
defines the module structure so future stages can add query decomposition,
retrieval, and synthesis logic without refactoring imports.
"""

from .langchain_client import LangChainClient, LangChainConfig

__all__ = [
    "LangChainClient",
    "LangChainConfig",
]

