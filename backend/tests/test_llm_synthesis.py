"""
Unit tests for the LLM synthesis service.
Tests the core functionality and error handling of the LLM service.
"""

import os
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.services.llm_synthesis import LLMSynthesisService, get_llm_synthesis_service
from src.api.v1.models import ExtractedContent, LLMResponse
from src.services.interfaces.llm_interface import (
    LLMResponse as BaseLLMResponse,
)
from src.services.providers.gemini_2_0_flash_provider import (
    GeminiLLMProvider,
)


class TestLLMSynthesisService:
    """Test cases for LLMSynthesisService."""

    def setup_method(self):
        """Set up test fixtures."""
        with patch(
            "src.core.config.sensitive_settings"
        ) as mock_settings:
            mock_settings.google_ai_api_key = "test_key"
            self.service = LLMSynthesisService()
        self.sample_content = [
            ExtractedContent(
                url="https://example.com/article1",
                title="Sample Article 1",
                extracted_text="This is sample content from article 1.",
                extraction_method="trafilatura",
                success=True,
                error_message=None,
            ),
            ExtractedContent(
                url="https://example.com/article2",
                title="Sample Article 2",
                extracted_text="This is sample content from article 2.",
                extraction_method="trafilatura",
                success=True,
                error_message=None,
            ),
        ]

    def test_init_without_api_key(self):
        """Test service initialization without API key."""
        with patch.dict(os.environ, {"GOOGLE_AI_API_KEY": ""}):
            service = LLMSynthesisService()
            # The service now always uses the intelligent system
            assert service.llm_provider is None

    def test_init_with_api_key(self):
        """Test service initialization with API key."""
        with patch.dict(os.environ, {"GOOGLE_AI_API_KEY": "test_key"}):
            service = LLMSynthesisService()
            # The service now always uses the intelligent system
            assert service.llm_provider is not None

    @pytest.mark.asyncio
    async def test_synthesize_answer_no_api_key(self):
        """Test synthesis attempt without API key."""
        with patch.dict(os.environ, {"GOOGLE_AI_API_KEY": ""}):
            service = LLMSynthesisService()
            result = await service.synthesize_answer(
                "test query", self.sample_content
            )

            assert not result.success
            assert (
                "Google Gemini provider not properly configured"
                in result.error_message
            )

    @pytest.mark.asyncio
    async def test_synthesize_answer_no_content(self):
        """Test synthesis attempt with no content."""
        with patch.dict(os.environ, {"GOOGLE_AI_API_KEY": "test_key"}):
            service = LLMSynthesisService()
            result = await service.synthesize_answer("test query", [])

            assert not result.success
            assert (
                "No content available for synthesis"
                in result.error_message
            )

    @pytest.mark.asyncio
    async def test_synthesize_answer_no_successful_content(self):
        """Test synthesis attempt with no successful content extractions."""
        failed_content = [
            ExtractedContent(
                url="https://example.com/failed",
                title="Failed Article",
                extracted_text="",
                extraction_method="trafilatura",
                success=False,
                error_message="Extraction failed",
            )
        ]

        with patch.dict(os.environ, {"GOOGLE_AI_API_KEY": "test_key"}):
            service = LLMSynthesisService()
            result = await service.synthesize_answer(
                "test query", failed_content
            )

            assert not result.success
            assert (
                "No successful content extractions available"
                in result.error_message
            )

    def test_combine_extracted_content(self):
        """Test content combination functionality."""
        combined = self.service._combine_extracted_content(
            self.sample_content
        )
        
        # Check that both sources are included
        assert "[Source 1]" in combined
        assert "[Source 1]" in combined
        assert "This is sample content from article 1." in combined
        assert "This is sample content from article 2." in combined
        assert "https://example.com/article1" in combined
        assert "https://example.com/article2" in combined

    @pytest.mark.asyncio
    async def test_synthesize_answer_success(self):
        """Test successful synthesis."""
        # Mock the intelligent synthesis service
        with patch("src.services.intelligent_llm_synthesis.IntelligentLLMSynthesisService") as mock_intelligent_class:
            mock_intelligent_service = MagicMock()
            mock_intelligent_service.synthesize_answer = AsyncMock(
                return_value=BaseLLMResponse(
                    content="This is a synthesized answer about AI.",
                    success=True,
                    tokens_used=50,
                )
            )
            mock_intelligent_class.return_value = mock_intelligent_service
            
            # Set environment variable and create service
            with patch.dict(os.environ, {"GOOGLE_AI_API_KEY": "test_key"}):
                service = LLMSynthesisService()
                
                result = await service.synthesize_answer(
                    "test query", self.sample_content
                )
                
                assert result.success
                assert "This is a synthesized answer about AI." in result.content

    @pytest.mark.asyncio
    async def test_synthesize_answer_llm_failure(self):
        """Test synthesis when LLM call fails."""
        # Mock the intelligent synthesis service to return failure
        with patch("src.services.intelligent_llm_synthesis.IntelligentLLMSynthesisService") as mock_intelligent_class:
            mock_intelligent_service = MagicMock()
            mock_intelligent_service.synthesize_answer = AsyncMock(
                return_value=BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="Intelligent synthesis failed",
                )
            )
            mock_intelligent_class.return_value = mock_intelligent_service
            
            # Set environment variable and create service
            with patch.dict(os.environ, {"GOOGLE_AI_API_KEY": "test_key"}):
                service = LLMSynthesisService()
                
                result = await service.synthesize_answer(
                    "test query", self.sample_content
                )
                
                assert not result.success
                assert "Intelligent synthesis failed" in result.error_message

    def test_get_llm_synthesis_service(self):
        """Test the convenience function."""
        service = get_llm_synthesis_service()
        assert isinstance(service, LLMSynthesisService)


class TestLLMResponse:
    """Test cases for LLMResponse dataclass."""

    def test_llm_response_creation(self):
        """Test LLMResponse object creation."""
        response = LLMResponse(
            answer="Test answer",
            success=True,
            error_message=None,
            tokens_used=100,
        )

        assert response.answer == "Test answer"
        assert response.success is True
        assert response.error_message is None
        assert response.tokens_used == 100

    def test_llm_response_with_error(self):
        """Test LLMResponse object creation with error."""
        response = LLMResponse(
            answer="",
            success=False,
            error_message="API error occurred",
            tokens_used=None,
        )

        assert response.answer == ""
        assert response.success is False
        assert response.error_message == "API error occurred"
        assert response.tokens_used is None
