"""
Tests for the Intelligent LLM Synthesis Service.

This module tests the new three-stage intelligent prompting system that
adapts response format and detail level based on question analysis.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.services.intelligent_llm_synthesis import (
    IntelligentLLMSynthesisService,
    QuestionAnalysis
)
from src.services.interfaces.llm_interface import LLMResponse


class TestQuestionAnalysis:
    """Test the QuestionAnalysis dataclass."""

    def test_question_analysis_creation(self):
        """Test creating a QuestionAnalysis instance."""
        analysis = QuestionAnalysis(
            question_type="FACTUAL",
            detail_level="LOW",
            recommended_format="CONCISE_TEXT",
            reasoning="Simple fact question",
            search_enhancement="capital of France official facts",
            source_priorities="Government websites, official databases",
            special_considerations="None"
        )
        
        assert analysis.question_type == "FACTUAL"
        assert analysis.detail_level == "LOW"
        assert analysis.recommended_format == "CONCISE_TEXT"
        assert analysis.reasoning == "Simple fact question"
        assert analysis.search_enhancement == "capital of France official facts"
        assert analysis.source_priorities == "Government websites, official databases"
        assert analysis.special_considerations == "None"


class TestIntelligentLLMSynthesisService:
    """Test the Intelligent LLM Synthesis Service."""

    @pytest.fixture
    def mock_llm_provider(self):
        """Create a mock LLM provider."""
        mock_provider = Mock()
        mock_provider.is_configured.return_value = True
        return mock_provider

    @pytest.fixture
    def service(self, mock_llm_provider):
        """Create a service instance with mocked dependencies."""
        with patch('os.getenv', return_value='test-api-key'):
            with patch('src.services.providers.gemini_2_0_flash_provider.GeminiLLMProvider') as mock_provider_class:
                mock_provider_class.return_value = mock_llm_provider
                service = IntelligentLLMSynthesisService()
                # Replace the real provider with our mock
                service.llm_provider = mock_llm_provider
                return service

    @pytest.fixture
    def mock_extracted_content(self):
        """Create mock extracted content."""
        from src.api.v1.models import ExtractedContent
        
        return [
            ExtractedContent(
                url="https://example1.com",
                title="Test Page 1",
                extracted_text="Test content from source 1",
                extraction_method="test",
                success=True
            ),
            ExtractedContent(
                url="https://example2.com",
                title="Test Page 2",
                extracted_text="Test content from source 2",
                extraction_method="test",
                success=True
            )
        ]

    def test_service_initialization(self, service):
        """Test service initialization."""
        assert service.llm_provider is not None
        assert service.llm_provider.is_configured()

    def test_parse_question_analysis_valid(self, service):
        """Test parsing valid question analysis response."""
        analysis_text = """
        **Question Type:** FACTUAL
        **Detail Level:** LOW
        **Recommended Format:** CONCISE_TEXT
        **Reasoning:** Simple fact question
        **Search Enhancement:** capital of France official facts
        **Source Priorities:** Government websites, official databases
        **Special Considerations:** None
        """
        
        analysis = service._parse_question_analysis(analysis_text)
        
        assert analysis.question_type == "FACTUAL"
        assert analysis.detail_level == "LOW"
        assert analysis.recommended_format == "CONCISE_TEXT"
        assert analysis.reasoning == "Simple fact question"
        assert analysis.search_enhancement == "capital of France official facts"
        assert analysis.source_priorities == "Government websites, official databases"
        assert analysis.special_considerations == "None"

    def test_parse_question_analysis_invalid(self, service):
        """Test parsing invalid question analysis response."""
        analysis_text = "Invalid format"
        
        analysis = service._parse_question_analysis(analysis_text)
        
        # Should return default values
        assert analysis.question_type == "EXPLANATORY"
        assert analysis.detail_level == "MEDIUM"
        assert analysis.recommended_format == "DETAILED_EXPLANATION"
        assert "Default analysis" in analysis.reasoning

    def test_combine_extracted_content(self, service, mock_extracted_content):
        """Test combining extracted content from multiple sources."""
        combined = service._combine_extracted_content(mock_extracted_content)
        
        assert "[Source 1]" in combined
        assert "[Source 2]" in combined
        assert "Test content from source 1" in combined
        assert "Test content from source 2" in combined
        assert "https://example1.com" in combined
        assert "https://example2.com" in combined

    def test_create_question_analysis_prompt(self, service):
        """Test creating question analysis prompt."""
        query = "What is the capital of France?"
        prompt = service._create_question_analysis_prompt(query)
        
        assert query in prompt
        assert "**Question Type:**" in prompt
        assert "**Detail Level:**" in prompt
        assert "**Recommended Format:**" in prompt

    def test_create_intelligent_synthesis_prompt(self, service):
        """Test creating intelligent synthesis prompt."""
        query = "What is the capital of France?"
        content = "Test content"
        analysis = QuestionAnalysis(
            question_type="FACTUAL",
            detail_level="LOW",
            recommended_format="CONCISE_TEXT",
            reasoning="Simple fact question",
            search_enhancement="capital of France official facts",
            source_priorities="Government websites, official databases",
            special_considerations="None"
        )
        
        prompt = service._create_intelligent_synthesis_prompt(query, content, analysis)
        
        assert query in prompt
        assert content in prompt
        assert analysis.question_type in prompt
        assert analysis.recommended_format in prompt
        assert analysis.search_enhancement in prompt
        assert analysis.source_priorities in prompt

    def test_create_adaptive_refinement_prompt(self, service):
        """Test creating adaptive refinement prompt."""
        query = "What is the capital of France?"
        content = "Test content"
        analysis = QuestionAnalysis(
            question_type="FACTUAL",
            detail_level="LOW",
            recommended_format="CONCISE_TEXT",
            reasoning="Simple fact question",
            search_enhancement="capital of France official facts",
            source_priorities="Government websites, official databases",
            special_considerations="None"
        )
        
        prompt = service._create_adaptive_refinement_prompt(query, content, analysis)
        
        assert query in prompt
        assert content in prompt
        assert analysis.question_type in prompt
        assert "Markdown Rules:" in prompt
        assert analysis.search_enhancement in prompt
        assert analysis.source_priorities in prompt

    @pytest.mark.asyncio
    async def test_analyze_question_success(self, service, mock_llm_provider):
        """Test successful question analysis."""
        mock_response = Mock()
        mock_response.success = True
        mock_response.content = """
        **Question Type:** FACTUAL
        **Detail Level:** LOW
        **Recommended Format:** CONCISE_TEXT
        **Reasoning:** Simple fact question
        **Search Enhancement:** capital of France official facts
        **Source Priorities:** Government websites, official databases
        **Special Considerations:** None
        """
        
        mock_llm_provider.generate_response = AsyncMock(return_value=mock_response)
        
        analysis = await service._analyze_question("What is the capital of France?")
        
        assert analysis is not None
        assert analysis.question_type == "FACTUAL"
        assert analysis.detail_level == "LOW"
        assert analysis.search_enhancement == "capital of France official facts"
        assert analysis.source_priorities == "Government websites, official databases"

    @pytest.mark.asyncio
    async def test_analyze_question_failure(self, service, mock_llm_provider):
        """Test failed question analysis."""
        mock_response = Mock()
        mock_response.success = False
        
        mock_llm_provider.generate_response = AsyncMock(return_value=mock_response)
        
        analysis = await service._analyze_question("What is the capital of France?")
        
        assert analysis is None

    @pytest.mark.asyncio
    async def test_intelligent_synthesis_success(self, service, mock_llm_provider):
        """Test successful intelligent synthesis."""
        mock_response = Mock()
        mock_response.success = True
        mock_response.content = "Test synthesized content"
        
        mock_llm_provider.generate_response = AsyncMock(return_value=mock_response)
        
        analysis = QuestionAnalysis(
            question_type="FACTUAL",
            detail_level="LOW",
            recommended_format="CONCISE_TEXT",
            reasoning="Simple fact question",
            search_enhancement="capital of France official facts",
            source_priorities="Government websites, official databases",
            special_considerations="None"
        )
        
        result = await service._intelligent_synthesis(
            "What is the capital of France?",
            "Test content",
            analysis
        )
        
        assert result is not None
        assert result.success is True
        assert result.content == "Test synthesized content"

    @pytest.mark.asyncio
    async def test_adaptive_refinement_success(self, service, mock_llm_provider):
        """Test successful adaptive refinement."""
        mock_response = Mock()
        mock_response.success = True
        mock_response.content = "Test refined content"
        
        mock_llm_provider.generate_response = AsyncMock(return_value=mock_response)
        
        analysis = QuestionAnalysis(
            question_type="FACTUAL",
            detail_level="LOW",
            recommended_format="CONCISE_TEXT",
            reasoning="Simple fact question",
            search_enhancement="capital of France official facts",
            source_priorities="Government websites, official databases",
            special_considerations="None"
        )
        
        result = await service._adaptive_refinement(
            "What is the capital of France?",
            "Test content",
            analysis
        )
        
        assert result is not None
        assert result.success is True
        assert result.content == "Test refined content"

    @pytest.mark.asyncio
    async def test_synthesize_answer_success(self, service, mock_llm_provider, mock_extracted_content):
        """Test successful end-to-end answer synthesis."""
        # Mock question analysis response
        analysis_response = Mock()
        analysis_response.success = True
        analysis_response.content = """
        **Question Type:** FACTUAL
        **Detail Level:** LOW
        **Recommended Format:** CONCISE_TEXT
        **Reasoning:** Simple fact question
        **Search Enhancement:** capital of France official facts
        **Source Priorities:** Government websites, official databases
        **Special Considerations:** None
        """
        
        # Mock synthesis response
        synthesis_response = Mock()
        synthesis_response.success = True
        synthesis_response.content = "Test synthesized content"
        
        # Mock refinement response
        refinement_response = Mock()
        refinement_response.success = True
        refinement_response.content = "Test final content"
        
        # Configure mock to return different responses for each call
        mock_llm_provider.generate_response = AsyncMock(side_effect=[
            analysis_response,
            synthesis_response,
            refinement_response
        ])
        
        result = await service.synthesize_answer(
            "What is the capital of France?",
            mock_extracted_content
        )
        
        assert result is not None
        assert result.success is True
        assert result.content == "Test final content"

    @pytest.mark.asyncio
    async def test_synthesize_answer_no_content(self, service):
        """Test synthesis with no extracted content."""
        result = await service.synthesize_answer("Test query", [])
        
        assert result is not None
        assert result.success is False
        assert "No content available" in result.error_message

    @pytest.mark.asyncio
    async def test_synthesize_answer_no_successful_extractions(self, service):
        """Test synthesis with no successful extractions."""
        from src.api.v1.models import ExtractedContent
        
        failed_content = [
            ExtractedContent(
                url="",
                title="",
                extracted_text="",
                extraction_method="test",
                success=False
            )
        ]
        
        result = await service.synthesize_answer("Test query", failed_content)
        
        assert result is not None
        assert result.success is False
        assert "No successful content extractions" in result.error_message
