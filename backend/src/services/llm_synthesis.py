"""
LLM Synthesis Service for generating intelligent, question-aware answers.

This service implements a three-stage intelligent prompting system:
1. Question Analysis: Determines optimal response format and detail level
2. Intelligent Synthesis: Generates content based on question type and user needs
3. Adaptive Refinement: Applies appropriate formatting for the chosen response style

This service uses the interface-based architecture to support multiple LLM providers.
"""

import logging
from typing import List, Optional

# Import the ExtractedContent model from the API layer
# Using a forward reference to avoid circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api.v1.models import ExtractedContent

from .interfaces.llm_interface import (
    LLMRequest,
    LLMResponse as BaseLLMResponse,
)
from .providers.gemini_2_0_flash_provider import GeminiLLMProvider
from .prompts import get_prompt

logger = logging.getLogger(__name__)


class LLMSynthesisService:
    """Service for intelligent, question-aware answer synthesis using Large Language Models."""

    def __init__(self) -> None:
        """Initialize the LLM synthesis service."""
        self.llm_provider: Optional[GeminiLLMProvider]
        
        # Initialize the LLM provider
        import os

        api_key = os.getenv("GOOGLE_AI_API_KEY")
        if api_key:
            self.llm_provider = GeminiLLMProvider(api_key=api_key)

            if not self.llm_provider.is_configured():
                logger.warning(
                    "Google Gemini provider not configured"
                )
        else:
            logger.warning(
                "No GOOGLE_AI_API_KEY environment variable found"
            )
            self.llm_provider = None

        logger.info("🧠 Using Intelligent Three-Stage Synthesis System")

    async def synthesize_answer(
        self, query: str, extracted_content: List["ExtractedContent"]
    ) -> "BaseLLMResponse":
        """
        Synthesize an intelligent, question-aware answer based on user query and extracted web content.

        Args:
            query: The user's search query
            extracted_content: List of extracted content from web pages

        Returns:
            LLMResponse containing the synthesized answer or error information
        """
        try:
            if not self.llm_provider or not self.llm_provider.is_configured():
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="Google Gemini provider not properly configured",
                )

            if not extracted_content:
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="No content available for synthesis",
                )

            # Filter successful extractions
            successful_content = [
                content
                for content in extracted_content
                if content.success
            ]

            if not successful_content:
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="No successful content extractions available",
                )

            # Combine extracted content
            combined_content = self._combine_extracted_content(
                successful_content
            )

            # Use the intelligent three-stage synthesis system
            return await self._intelligent_synthesis(query, combined_content)

        except Exception as e:
            logger.error(f"❌ Error in LLM synthesis: {str(e)}")
            return BaseLLMResponse(
                content="",
                success=False,
                error_message=f"Synthesis error: {str(e)}",
            )

    async def _intelligent_synthesis(
        self, query: str, combined_content: str
    ) -> "BaseLLMResponse":
        """
        Use the intelligent three-stage synthesis system.
        
        Args:
            query: The user's search query
            combined_content: Combined extracted content from web sources
            
        Returns:
            LLMResponse with intelligently synthesized answer
        """
        try:
            # Import here to avoid circular imports
            from .intelligent_llm_synthesis import IntelligentLLMSynthesisService
            
            intelligent_service = IntelligentLLMSynthesisService()
            
            # Convert combined_content back to ExtractedContent format for the intelligent service
            # This is a temporary workaround - in the future, we should refactor to use a common format
            from ..api.v1.models import ExtractedContent
            
            # Create mock ExtractedContent objects for the intelligent service
            mock_extracted_content = [
                ExtractedContent(
                    url="",
                    title="Combined Content",
                    extracted_text=combined_content,
                    extraction_method="combined",
                    success=True
                )
            ]
            
            return await intelligent_service.synthesize_answer(query, mock_extracted_content)
            
        except Exception as e:
            logger.error(f"❌ Error in intelligent synthesis: {str(e)}")
            return BaseLLMResponse(
                content="",
                success=False,
                error_message=f"Intelligent synthesis failed: {str(e)}",
            )

    def _combine_extracted_content(
        self, content_list: List["ExtractedContent"]
    ) -> str:
        """
        Combine extracted content from multiple sources into a single string.

        Args:
            content_list: List of successfully extracted content

        Returns:
            Combined content string with source attribution
        """
        combined = []
        
        for i, content in enumerate(content_list, 1):
            if content.extracted_text:
                # Add source identifier
                source_info = f"[Source {i}]"
                if content.url:
                    source_info += f" {content.url}"
                
                combined.append(f"{source_info}\n{content.extracted_text}\n")
        
        return "\n".join(combined)

    def is_configured(self) -> bool:
        """Check if the service is properly configured."""
        return self.llm_provider is not None


def get_llm_synthesis_service() -> LLMSynthesisService:
    """Get an instance of the LLM synthesis service."""
    return LLMSynthesisService()


def is_configured() -> bool:
    """Check if the LLM synthesis service is properly configured."""
    try:
        service = get_llm_synthesis_service()
        return service.llm_provider is not None
    except Exception:
        return False
