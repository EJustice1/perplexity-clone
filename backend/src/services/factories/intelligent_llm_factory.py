"""
Factory for creating intelligent LLM synthesis services.

This factory provides a centralized way to create and configure
intelligent LLM synthesis services with different providers.
"""

from typing import Optional
from ..intelligent_llm_synthesis import IntelligentLLMSynthesisService


class IntelligentLLMFactory:
    """Factory for creating intelligent LLM synthesis services."""

    @staticmethod
    def create_intelligent_llm_service() -> IntelligentLLMSynthesisService:
        """
        Create a new intelligent LLM synthesis service.

        Returns:
            Configured IntelligentLLMSynthesisService instance
        """
        return IntelligentLLMSynthesisService()

    @staticmethod
    def create_intelligent_llm_service_with_config(
        api_key: Optional[str] = None,
        provider_name: Optional[str] = None
    ) -> IntelligentLLMSynthesisService:
        """
        Create a new intelligent LLM synthesis service with custom configuration.

        Args:
            api_key: Optional API key for the LLM provider
            provider_name: Optional provider name (currently only supports Gemini)

        Returns:
            Configured IntelligentLLMSynthesisService instance
        """
        # Set environment variable if provided
        if api_key:
            import os
            os.environ["GOOGLE_AI_API_KEY"] = api_key

        return IntelligentLLMSynthesisService()
