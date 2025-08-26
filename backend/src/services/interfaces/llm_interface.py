"""
LLM Provider Interface - Defines the contract for all LLM implementations.

This interface allows for easy switching between different LLM providers
(OpenAI, Google Gemini, Anthropic Claude, etc.) without changing the core business logic.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Any
from enum import Enum


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    OPENAI = "openai"
    GOOGLE_GEMINI = "google_gemini"
    ANTHROPIC = "anthropic"
    AZURE_OPENAI = "azure_openai"


@dataclass
class LLMRequest:
    """Request object for LLM operations."""

    prompt: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    model: Optional[str] = None
    system_message: Optional[str] = None


@dataclass
class LLMResponse:
    """Response object from LLM operations."""

    content: str
    success: bool
    error_message: Optional[str] = None
    tokens_used: Optional[int] = None
    model_used: Optional[str] = None
    provider: Optional[str] = None
    finish_reason: Optional[str] = None


class LLMProviderInterface(ABC):
    """
    Abstract base class for all LLM providers.

    All LLM implementations must inherit from this class and implement
    the required methods to ensure consistent behavior across providers.
    """

    @abstractmethod
    def __init__(self, api_key: str, **kwargs: Any) -> None:
        """
        Initialize the LLM provider with necessary credentials.

        Args:
            api_key: API key for the LLM provider
            **kwargs: Additional provider-specific configuration
        """
        pass

    @abstractmethod
    async def generate_response(
        self, request: LLMRequest
    ) -> LLMResponse:
        """
        Generate a response using the LLM.

        Args:
            request: LLM request containing prompt and configuration

        Returns:
            LLMResponse containing the generated content and metadata
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
    def get_supported_models(self) -> List[str]:
        """
        Get list of models supported by this provider.

        Returns:
            List of model names supported by this provider
        """
        pass

    @abstractmethod
    def validate_model(self, model: str) -> bool:
        """
        Validate if a model is supported by this provider.

        Args:
            model: Model name to validate

        Returns:
            True if model is supported, False otherwise
        """
        pass
