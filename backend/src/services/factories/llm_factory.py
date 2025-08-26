"""
LLM Service Factory - Creates and manages LLM provider instances.

This factory creates Gemini LLM provider instances, which is the only
LLM provider supported in the system.
"""

import logging
import os
from typing import Optional, Dict, Any

from ..interfaces.llm_interface import LLMProviderInterface
from ..providers.gemini_2_0_flash_provider import GeminiLLMProvider

logger = logging.getLogger(__name__)


class LLMServiceFactory:
    """Factory for creating LLM provider instances."""

    # Only Gemini provider is supported
    _providers = {
        "gemini": GeminiLLMProvider,
    }

    # Singleton instances
    _instances: Dict[str, LLMProviderInterface] = {}

    @classmethod
    def create_provider(
        cls, provider: str, api_key: str, **kwargs: Any
    ) -> LLMProviderInterface:
        """
        Create a new LLM provider instance.

        Args:
            provider: LLM provider type
            api_key: API key for the provider
            **kwargs: Additional provider-specific configuration

        Returns:
            LLM provider instance

        Raises:
            ValueError: If provider is not supported
            Exception: If provider initialization fails
        """
        if provider not in cls._providers:
            raise ValueError(f"Unsupported LLM provider: {provider}")

        provider_class = cls._providers[provider]

        try:
            instance = provider_class(api_key=api_key, **kwargs)
            logger.info(f"Created {provider} LLM provider instance")
            return instance
        except Exception as e:
            logger.error(
                f"Failed to create {provider} LLM provider: {str(e)}"
            )
            raise

    @classmethod
    def get_provider(
        cls, provider: Optional[str] = None, **kwargs: Any
    ) -> Optional[LLMProviderInterface]:
        """
        Get or create an LLM provider instance (singleton pattern).

        Args:
            provider: LLM provider type (defaults to configured provider)
            **kwargs: Additional provider-specific configuration

        Returns:
            LLM provider instance or None if not configured
        """
        # Determine provider from environment or parameter
        if provider is None:
            provider = os.getenv("LLM_PROVIDER", "gemini").lower()

        # Check if instance already exists
        provider_key = f"{provider}_{hash(frozenset(kwargs.items()) if kwargs else frozenset())}"
        if provider_key in cls._instances:
            return cls._instances[provider_key]

        # Get API key from environment
        api_key = cls._get_api_key_for_provider(provider)
        if not api_key:
            logger.warning(
                f"No API key found for {provider} provider"
            )
            return None

        try:
            # Create new instance
            instance = cls.create_provider(
                provider, api_key, **kwargs
            )
            cls._instances[provider_key] = instance
            return instance
        except Exception as e:
            logger.error(
                f"Failed to get {provider} provider: {str(e)}"
            )
            return None

    @classmethod
    def _get_api_key_for_provider(
        cls, provider: str
    ) -> Optional[str]:
        """
        Get API key for a specific provider from environment variables.

        Args:
            provider: LLM provider type

        Returns:
            API key string or None if not found
        """
        # Only Gemini is supported, so only check for GOOGLE_AI_API_KEY
        return os.getenv("GOOGLE_AI_API_KEY")

    @classmethod
    def get_available_providers(cls) -> list[str]:
        """
        Get list of available LLM providers.

        Returns:
            List of available provider types
        """
        return list(cls._providers.keys())

    @classmethod
    def is_provider_available(cls, provider: str) -> bool:
        """
        Check if a provider is available and configured.

        Args:
            provider: LLM provider type to check

        Returns:
            True if provider is available and has API key, False otherwise
        """
        if provider not in cls._providers:
            return False

        api_key = cls._get_api_key_for_provider(provider)
        return bool(api_key)

    @classmethod
    def clear_instances(cls) -> None:
        """Clear all cached provider instances."""
        cls._instances.clear()
        logger.info("Cleared all LLM provider instances")


# Convenience function for getting the default LLM provider
def get_llm_provider(**kwargs: Any) -> Optional[LLMProviderInterface]:
    """
    Get the default LLM provider instance.

    Args:
        **kwargs: Additional provider-specific configuration

    Returns:
        LLM provider instance or None if not configured
    """
    return LLMServiceFactory.get_provider(**kwargs)
