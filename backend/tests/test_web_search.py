"""
Tests for the web search service.
Tests the web search functionality and provider implementations.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

# Add the src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.web_search import (
    WebSearchResult,
    WebSearchProvider,
    SerperWebSearchProvider,
    WebSearchService,
    create_web_search_service,
    get_web_search_service,
)


class TestWebSearchResult:
    """Test WebSearchResult data structure."""

    def test_web_search_result_creation(self):
        """Test creating a WebSearchResult instance."""
        result = WebSearchResult(
            title="Test Title",
            url="https://example.com",
            snippet="Test snippet",
            source="test_source",
        )

        assert result.title == "Test Title"
        assert result.url == "https://example.com"
        assert result.snippet == "Test snippet"
        assert result.source == "test_source"

    def test_web_search_result_default_source(self):
        """Test WebSearchResult with default source."""
        result = WebSearchResult(
            title="Test Title", url="https://example.com", snippet="Test snippet"
        )

        assert result.source == "web_search"

    def test_web_search_result_to_dict(self):
        """Test converting WebSearchResult to dictionary."""
        result = WebSearchResult(
            title="Test Title",
            url="https://example.com",
            snippet="Test snippet",
            source="test_source",
        )

        result_dict = result.to_dict()

        assert result_dict == {
            "title": "Test Title",
            "url": "https://example.com",
            "snippet": "Test snippet",
            "source": "test_source",
        }


class TestSerperWebSearchProvider:
    """Test SerperWebSearchProvider implementation."""

    def test_serper_provider_initialization(self):
        """Test SerperWebSearchProvider initialization."""
        provider = SerperWebSearchProvider("test_api_key")

        assert provider.api_key == "test_api_key"
        assert provider.base_url == "https://google.serper.dev/search"
        assert provider.headers == {
            "X-API-KEY": "test_api_key",
            "Content-Type": "application/json",
        }

    @pytest.mark.asyncio
    async def test_serper_search_success(self):
        """Test successful search with Serper provider."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "organic": [
                {
                    "title": "Test Result 1",
                    "link": "https://example1.com",
                    "snippet": "Test snippet 1",
                },
                {
                    "title": "Test Result 2",
                    "link": "https://example2.com",
                    "snippet": "Test snippet 2",
                },
            ]
        }
        mock_response.raise_for_status.return_value = None

        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.post.return_value = mock_response

        with patch("httpx.AsyncClient", return_value=mock_client):
            provider = SerperWebSearchProvider("test_api_key")
            results = await provider.search("test query", max_results=2)

            assert len(results) == 2
            assert results[0].title == "Test Result 1"
            assert results[0].url == "https://example1.com"
            assert results[0].snippet == "Test snippet 1"
            assert results[1].title == "Test Result 2"
            assert results[1].url == "https://example2.com"
            assert results[1].snippet == "Test snippet 2"

    @pytest.mark.asyncio
    async def test_serper_search_http_error(self):
        """Test Serper provider with HTTP error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"

        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.post.return_value = mock_response
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")

        with patch("httpx.AsyncClient", return_value=mock_client):
            provider = SerperWebSearchProvider("test_api_key")

            with pytest.raises(Exception, match="Web search failed unexpectedly"):
                await provider.search("test query")


class TestWebSearchService:
    """Test WebSearchService wrapper."""

    def test_web_search_service_initialization(self):
        """Test WebSearchService initialization."""
        mock_provider = MagicMock(spec=WebSearchProvider)
        service = WebSearchService(mock_provider)

        assert service.provider == mock_provider

    @pytest.mark.asyncio
    async def test_web_search_service_search_success(self):
        """Test successful search through WebSearchService."""
        mock_provider = MagicMock(spec=WebSearchProvider)
        mock_results = [
            WebSearchResult("Title 1", "https://example1.com", "Snippet 1"),
            WebSearchResult("Title 2", "https://example2.com", "Snippet 2"),
        ]
        mock_provider.search.return_value = mock_results

        service = WebSearchService(mock_provider)
        results = await service.search("test query", max_results=2)

        assert results == mock_results
        mock_provider.search.assert_called_once_with("test query", 2)

    @pytest.mark.asyncio
    async def test_web_search_service_empty_query(self):
        """Test WebSearchService with empty query."""
        mock_provider = MagicMock(spec=WebSearchProvider)
        service = WebSearchService(mock_provider)

        with pytest.raises(ValueError, match="Search query cannot be empty"):
            await service.search("", max_results=5)

    @pytest.mark.asyncio
    async def test_web_search_service_invalid_max_results(self):
        """Test WebSearchService with invalid max_results."""
        mock_provider = MagicMock(spec=WebSearchProvider)
        service = WebSearchService(mock_provider)

        with pytest.raises(ValueError, match="max_results must be positive"):
            await service.search("test query", max_results=0)


class TestWebSearchServiceFactory:
    """Test web search service factory functions."""

    @patch("src.services.web_search.settings")
    def test_create_web_search_service_success(self, mock_settings):
        """Test successful creation of web search service."""
        mock_settings.serper_api_key = "test_api_key"

        service = create_web_search_service()

        assert isinstance(service, WebSearchService)
        assert isinstance(service.provider, SerperWebSearchProvider)
        assert service.provider.api_key == "test_api_key"

    @patch("src.services.web_search.settings")
    def test_create_web_search_service_missing_api_key(self, mock_settings):
        """Test creation of web search service with missing API key."""
        mock_settings.serper_api_key = None

        with pytest.raises(
            ValueError,
            match="SERPER_API_KEY environment variable is required for web search",
        ):
            create_web_search_service()

    @patch("src.services.web_search.create_web_search_service")
    def test_get_web_search_service_singleton(self, mock_create):
        """Test that get_web_search_service returns singleton instance."""
        mock_service = MagicMock()
        mock_create.return_value = mock_service

        # Reset the singleton for testing
        from src.services.web_search import web_search_service
        import src.services.web_search
        src.services.web_search.web_search_service = None

        # First call should create the service
        service1 = get_web_search_service()
        assert service1 == mock_service
        mock_create.assert_called_once()

        # Second call should return the same instance
        service2 = get_web_search_service()
        assert service2 == service1
        assert mock_create.call_count == 1  # Should not be called again
