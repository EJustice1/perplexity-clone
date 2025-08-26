"""
Tests for the query enhancement service.
Tests the query enhancement functionality and provider implementations.
"""

import os
import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

# Add the src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.query_enhancement import (
    QueryEnhancementService,
    create_query_enhancement_service,
    get_query_enhancement_service,
)
from src.services.interfaces.query_enhancement_interface import (
    QueryEnhancementRequest,
    QueryEnhancementResponse,
)


class TestQueryEnhancementService:
    """Test QueryEnhancementService functionality."""

    def test_service_initialization(self):
        """Test QueryEnhancementService initialization."""
        service = QueryEnhancementService()
        assert service is not None

    @patch.dict(os.environ, {"GOOGLE_AI_API_KEY": "test_api_key"})
    def test_service_initialization_with_api_key(self):
        """Test service initialization when API key is available."""
        with patch("src.services.providers.gemini_2_0_flash_lite_provider.Gemini2FlashLiteProvider") as mock_provider_class:
            mock_provider = MagicMock()
            mock_provider_class.return_value = mock_provider
            
            service = QueryEnhancementService()
            assert service.provider is not None

    @patch.dict(os.environ, {"GOOGLE_AI_API_KEY": ""})
    def test_service_initialization_without_api_key(self):
        """Test service initialization when no API key is available."""
        service = QueryEnhancementService()
        assert service.provider is None

    def test_is_configured_false(self):
        """Test is_configured when provider is not available."""
        service = QueryEnhancementService()
        # Mock the provider to be None
        service.provider = None
        assert not service.is_configured()

    def test_get_provider_name_none(self):
        """Test get_provider_name when no provider is available."""
        service = QueryEnhancementService()
        service.provider = None
        assert service.get_provider_name() == "none"

    @pytest.mark.asyncio
    async def test_enhance_query_no_provider(self):
        """Test enhance_query when no provider is available."""
        service = QueryEnhancementService()
        service.provider = None
        
        response = await service.enhance_query("test query")
        
        assert response.success is False
        assert response.enhanced_query == "test query"
        assert "not configured" in response.error_message

    @pytest.mark.asyncio
    async def test_enhance_query_empty_query(self):
        """Test enhance_query with empty query."""
        service = QueryEnhancementService()
        
        response = await service.enhance_query("")
        
        assert response.success is False
        assert response.enhanced_query == ""
        assert "empty query" in response.error_message

    @pytest.mark.asyncio
    async def test_enhance_query_whitespace_only(self):
        """Test enhance_query with whitespace-only query."""
        service = QueryEnhancementService()
        
        response = await service.enhance_query("   ")
        
        assert response.success is False
        assert response.enhanced_query == "   "
        assert "empty query" in response.error_message

    @pytest.mark.asyncio
    async def test_enhance_query_with_provider_success(self):
        """Test enhance_query when provider succeeds."""
        service = QueryEnhancementService()
        
        # Mock provider
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        
        # Mock the async enhance_query method
        async def mock_enhance_query(request):
            return QueryEnhancementResponse(
                enhanced_query="enhanced test query",
                success=True,
                error_message=None,
            )
        
        mock_provider.enhance_query = mock_enhance_query
        service.provider = mock_provider
        
        response = await service.enhance_query("test query")
        
        assert response.success is True
        assert response.enhanced_query == "enhanced test query"
        assert response.error_message is None

    @pytest.mark.asyncio
    async def test_enhance_query_with_provider_failure(self):
        """Test enhance_query when provider fails."""
        service = QueryEnhancementService()
        
        # Mock provider
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        
        # Mock the async enhance_query method
        async def mock_enhance_query(request):
            from src.services.interfaces.query_enhancement_interface import QueryEnhancementResponse
            return QueryEnhancementResponse(
                enhanced_query="test query",
                success=False,
                error_message="Provider error",
            )
        
        mock_provider.enhance_query = mock_enhance_query
        service.provider = mock_provider
        
        response = await service.enhance_query("test query")
        
        assert response.success is False
        assert response.enhanced_query == "test query"
        assert response.error_message == "Provider error"

    @pytest.mark.asyncio
    async def test_enhance_query_provider_exception(self):
        """Test enhance_query when provider raises an exception."""
        service = QueryEnhancementService()
        
        # Mock provider
        mock_provider = MagicMock()
        mock_provider.is_configured.return_value = True
        mock_provider.enhance_query.side_effect = Exception("Provider exception")
        service.provider = mock_provider
        
        response = await service.enhance_query("test query")
        
        assert response.success is False
        assert response.enhanced_query == "test query"
        assert "Provider exception" in response.error_message


class TestQueryEnhancementServiceFactory:
    """Test query enhancement service factory functions."""

    def test_create_query_enhancement_service(self):
        """Test successful creation of query enhancement service."""
        service = create_query_enhancement_service()
        assert isinstance(service, QueryEnhancementService)

    @patch("src.services.query_enhancement.create_query_enhancement_service")
    def test_get_query_enhancement_service_singleton(self, mock_create):
        """Test that get_query_enhancement_service returns singleton instance."""
        mock_service = MagicMock()
        mock_create.return_value = mock_service

        # Reset the singleton for testing
        from src.services.query_enhancement import _query_enhancement_service
        import src.services.query_enhancement

        src.services.query_enhancement._query_enhancement_service = None

        # First call should create the service
        service1 = get_query_enhancement_service()
        assert service1 == mock_service
        mock_create.assert_called_once()

        # Second call should return the same instance
        service2 = get_query_enhancement_service()
        assert service2 == service1
        assert mock_create.call_count == 1  # Should not be called again
