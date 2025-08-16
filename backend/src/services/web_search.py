"""
Web search service layer.
Contains business logic for web search operations with an implementation-agnostic interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import httpx
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)


class WebSearchResult:
    """Data structure for web search results."""

    def __init__(self, title: str, url: str, snippet: str, source: str = "web_search"):
        self.title = title
        self.url = url
        self.snippet = snippet
        self.source = source

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for JSON serialization."""
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
        }


class WebSearchProvider(ABC):
    """Abstract interface for web search providers."""

    @abstractmethod
    async def search(self, query: str, max_results: int = 5) -> List[WebSearchResult]:
        """
        Perform a web search for the given query.

        Args:
            query: The search query to execute
            max_results: Maximum number of results to return

        Returns:
            List of WebSearchResult objects

        Raises:
            Exception: If the search fails
        """
        pass


class SerperWebSearchProvider(WebSearchProvider):
    """Serper.dev web search provider implementation."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://google.serper.dev/search"
        self.headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

    async def search(self, query: str, max_results: int = 5) -> List[WebSearchResult]:
        """
        Perform a web search using Serper.dev API.

        Args:
            query: The search query to execute
            max_results: Maximum number of results to return

        Returns:
            List of WebSearchResult objects

        Raises:
            Exception: If the search fails
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers=self.headers,
                    json={"q": query, "num": max_results},
                    timeout=30.0,
                )
                response.raise_for_status()

                data = response.json()
                results = []

                # Extract organic search results
                if "organic" in data:
                    for item in data["organic"][:max_results]:
                        result = WebSearchResult(
                            title=item.get("title", "No title"),
                            url=item.get("link", ""),
                            snippet=item.get("snippet", "No description available"),
                        )
                        results.append(result)

                logger.info(
                    f"Serper search completed for query '{query}', found {len(results)} results"
                )
                return results

        except httpx.HTTPStatusError as e:
            logger.error(
                f"Serper API HTTP error: {e.response.status_code} - {e.response.text}"
            )
            raise Exception(f"Web search failed with status {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Serper API request error: {str(e)}")
            raise Exception("Web search request failed")
        except Exception as e:
            logger.error(f"Unexpected error in Serper search: {str(e)}")
            raise Exception("Web search failed unexpectedly")


class WebSearchService:
    """Service class for web search operations."""

    def __init__(self, provider: WebSearchProvider):
        self.provider = provider

    async def search(self, query: str, max_results: int = 5) -> List[WebSearchResult]:
        """
        Perform a web search using the configured provider.

        Args:
            query: The search query to execute
            max_results: Maximum number of results to return

        Returns:
            List of WebSearchResult objects

        Raises:
            ValueError: If query is empty or invalid
            Exception: If the search fails
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")

        if max_results <= 0:
            raise ValueError("max_results must be positive")

        return await self.provider.search(query.strip(), max_results)


# Factory function to create the appropriate web search service
def create_web_search_service() -> WebSearchService:
    """Create and configure the web search service based on environment."""
    api_key = settings.serper_api_key

    if not api_key:
        raise ValueError(
            "SERPER_API_KEY environment variable is required for web search"
        )

    provider = SerperWebSearchProvider(api_key)
    return WebSearchService(provider)


# Global service instance (will be initialized when needed)
web_search_service: Optional[WebSearchService] = None


def get_web_search_service() -> WebSearchService:
    """Get the global web search service instance, creating it if necessary."""
    global web_search_service

    if web_search_service is None:
        web_search_service = create_web_search_service()

    return web_search_service
