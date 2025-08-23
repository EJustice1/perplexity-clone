"""
Unit tests for the LLM synthesis service.
Tests the core functionality and error handling of the LLM service.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.services.llm_synthesis import LLMSynthesisService, LLMResponse
from src.api.v1.models import ExtractedContent
from src.services.interfaces.llm_interface import LLMResponse as BaseLLMResponse
from src.services.providers.gemini_llm_provider import GeminiLLMProvider


class TestLLMSynthesisService:
    """Test cases for LLMSynthesisService."""

    def setup_method(self):
        """Set up test fixtures."""
        with patch('src.core.config.sensitive_settings') as mock_settings:
            mock_settings.google_ai_api_key = "test_key"
            self.service = LLMSynthesisService()
        self.sample_content = [
            ExtractedContent(
                url="https://example.com/article1",
                title="Sample Article 1",
                extracted_text="This is sample content from article 1.",
                extraction_method="trafilatura",
                success=True,
                error_message=None
            ),
            ExtractedContent(
                url="https://example.com/article2",
                title="Sample Article 2",
                extracted_text="This is sample content from article 2.",
                extraction_method="trafilatura",
                success=True,
                error_message=None
            )
        ]

    def test_init_without_api_key(self):
        """Test service initialization without API key."""
        with patch('src.core.config.sensitive_settings') as mock_settings:
            mock_settings.google_ai_api_key = None
            service = LLMSynthesisService()
            assert not service.is_configured()

    def test_init_with_api_key(self):
        """Test service initialization with API key."""
        with patch('src.core.config.sensitive_settings') as mock_settings:
            mock_settings.google_ai_api_key = "test_key"
            service = LLMSynthesisService()
            assert service.is_configured()

    @pytest.mark.asyncio
    async def test_synthesize_answer_no_api_key(self):
        """Test synthesis attempt without API key."""
        with patch('src.core.config.sensitive_settings') as mock_settings:
            mock_settings.google_ai_api_key = None
            service = LLMSynthesisService()
            result = await service.synthesize_answer("test query", self.sample_content)
            
            assert not result.success
            assert "Google Gemini provider not properly configured" in result.error_message

    @pytest.mark.asyncio
    async def test_synthesize_answer_no_content(self):
        """Test synthesis attempt with no content."""
        with patch('src.core.config.sensitive_settings') as mock_settings:
            mock_settings.google_ai_api_key = "test_key"
            service = LLMSynthesisService()
            result = await service.synthesize_answer("test query", [])
            
            assert not result.success
            assert "No content available for synthesis" in result.error_message

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
                error_message="Extraction failed"
            )
        ]
        
        with patch('src.core.config.sensitive_settings') as mock_settings:
            mock_settings.google_ai_api_key = "test_key"
            service = LLMSynthesisService()
            result = await service.synthesize_answer("test query", failed_content)
            
            assert not result.success
            assert "No successful content extractions available" in result.error_message

    def test_combine_extracted_content(self):
        """Test content combination functionality."""
        combined = self.service._combine_extracted_content(self.sample_content)
        
        assert "Source 1 (Sample Article 1):" in combined
        assert "Source 2 (Sample Article 2):" in combined
        assert "This is sample content from article 1." in combined
        assert "This is sample content from article 2." in combined

    def test_create_rag_prompt(self):
        """Test RAG prompt creation."""
        query = "What is artificial intelligence?"
        content = "Sample content about AI."
        
        prompt = self.service._create_rag_prompt(query, content)
        
        assert query in prompt
        assert content in prompt
        assert "Based ONLY on the provided text below" in prompt
        assert "Do not use any outside knowledge" in prompt

    @pytest.mark.asyncio
    async def test_synthesize_answer_success(self):
        """Test successful synthesis."""
        with patch('src.core.config.sensitive_settings') as mock_settings:
            mock_settings.google_ai_api_key = "test_key"
            
            # Mock the Gemini provider
            with patch('src.services.llm_synthesis.GeminiLLMProvider') as mock_provider_class:
                mock_provider = MagicMock()
                mock_provider.is_configured.return_value = True
                
                # Create an async mock for generate_response
                async def mock_generate_response(request):
                    return BaseLLMResponse(
                        content="This is a synthesized answer about AI.",
                        success=True,
                        tokens_used=50
                    )
                
                mock_provider.generate_response = mock_generate_response
                mock_provider_class.return_value = mock_provider
                
                service = LLMSynthesisService()
                result = await service.synthesize_answer("test query", self.sample_content)
                
                assert result.success
                assert "This is a synthesized answer about AI." in result.answer
                assert result.error_message is None
                assert result.tokens_used == 50

    @pytest.mark.asyncio
    async def test_synthesize_answer_llm_failure(self):
        """Test synthesis when LLM call fails."""
        with patch('src.core.config.sensitive_settings') as mock_settings:
            mock_settings.google_ai_api_key = "test_key"
            
            # Mock the Gemini provider
            with patch('src.services.llm_synthesis.GeminiLLMProvider') as mock_provider_class:
                mock_provider = MagicMock()
                mock_provider.is_configured.return_value = True
                
                # Create an async mock for generate_response that returns failure
                async def mock_generate_response(request):
                    return BaseLLMResponse(
                        content="",
                        success=False,
                        error_message="LLM API error"
                    )
                
                mock_provider.generate_response = mock_generate_response
                mock_provider_class.return_value = mock_provider
                
                service = LLMSynthesisService()
                result = await service.synthesize_answer("test query", self.sample_content)
                
                assert not result.success
                assert "LLM API error" in result.error_message

    def test_is_configured(self):
        """Test configuration check method."""
        # Test without API key
        with patch('src.core.config.sensitive_settings') as mock_settings:
            mock_settings.google_ai_api_key = None
            service = LLMSynthesisService()
            assert not service.is_configured()
        
        # Test with API key
        with patch('src.core.config.sensitive_settings') as mock_settings:
            mock_settings.google_ai_api_key = "test_key"
            service = LLMSynthesisService()
            assert service.is_configured()


class TestLLMResponse:
    """Test cases for LLMResponse dataclass."""

    def test_llm_response_creation(self):
        """Test LLMResponse object creation."""
        response = LLMResponse(
            answer="Test answer",
            success=True,
            error_message=None,
            tokens_used=100
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
            tokens_used=None
        )
        
        assert response.answer == ""
        assert response.success is False
        assert response.error_message == "API error occurred"
        assert response.tokens_used is None
