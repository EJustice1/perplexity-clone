"""
Web Search Provider Interface - Defines the contract for all web search implementations.

This interface allows for easy switching between different web search providers
(Serper, Google Custom Search, Bing, etc.) without changing the core business logic.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Any
from enum import Enum


class WebSearchProvider(str, Enum):
    """Supported web search providers."""

    SERPER = "serper"
    GOOGLE_CUSTOM_SEARCH = "google_custom_search"
    BING_SEARCH = "bing_search"
    BRAVE_SEARCH = "brave_search"


@dataclass
class WebSearchRequest:
    """Request object for web search operations."""

    query: str
    max_results: int = 10
    language: Optional[str] = None
    country: Optional[str] = None
    search_type: Optional[str] = "web"  # web, images, news, etc.


@dataclass
class WebSearchResult:
    """Individual search result."""

    title: str
    url: str
    snippet: str
    source: str
    rank: Optional[int] = None
    date: Optional[str] = None


@dataclass
class WebSearchResponse:
    """Response object from web search operations."""

    results: List[WebSearchResult]
    success: bool
    total_results: Optional[int] = None
    search_time: Optional[float] = None
    error_message: Optional[str] = None
    provider: Optional[str] = None
    query_used: Optional[str] = None


class WebSearchProviderInterface(ABC):
    """
    Abstract base class for all web search providers.

    All web search implementations must inherit from this class and implement
    the required methods to ensure consistent behavior across providers.
    """

    @abstractmethod
    def __init__(self, api_key: str, **kwargs: Any) -> None:
        """
        Initialize the web search provider with necessary credentials.

        Args:
            api_key: API key for the search provider
            **kwargs: Additional provider-specific configuration
        """
        pass

    @abstractmethod
    async def search(
        self, request: WebSearchRequest
    ) -> WebSearchResponse:
        """
        Perform a web search.

        Args:
            request: Web search request containing query and configuration

        Returns:
            WebSearchResponse containing search results and metadata
        """
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """
        Check if the provider is properly configured.

        Returns:
            True if the provider is ready to use, False otherwise
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the name of the provider.

        Returns:
            String identifier for this provider
        """
        pass

    @abstractmethod
    def get_supported_search_types(self) -> List[str]:
        """
        Get list of search types supported by this provider.

        Returns:
            List of supported search types (web, images, news, etc.)
        """
        pass

    @abstractmethod
    def validate_search_type(self, search_type: str) -> bool:
        """
        Validate if a search type is supported by this provider.

        Args:
            search_type: Search type to validate

        Returns:
            True if search type is supported, False otherwise
        """
        pass
