"""
Service interfaces for external API integrations.
This module defines the contracts that all service implementations must follow.
"""

from .llm_interface import LLMProvider, LLMRequest, LLMResponse
from .web_search_interface import WebSearchProvider, WebSearchRequest, WebSearchResponse
from .content_extractor_interface import ContentExtractorProvider, ContentExtractionRequest, ContentExtractionResponse

__all__ = [
    "LLMProvider",
    "LLMRequest", 
    "LLMResponse",
    "WebSearchProvider",
    "WebSearchRequest",
    "WebSearchResponse", 
    "ContentExtractorProvider",
    "ContentExtractionRequest",
    "ContentExtractionResponse",
]
