"""
Content Extractor Service Factory - Creates and manages content extractor provider instances.

This factory handles the creation of different content extractor providers based on configuration,
providing a single interface for content extraction service instantiation.
"""

import logging
import os
from typing import Optional, Dict, Any, List

from ..interfaces.content_extractor_interface import (
    ContentExtractorProviderInterface,
    ContentExtractorProvider,
)
from ..providers.trafilatura_provider import (
    TrafilaturaContentExtractor,
)
from ..providers.beautifulsoup4_provider import (
    BeautifulSoupContentExtractor,
)

logger = logging.getLogger(__name__)


class ContentExtractorServiceFactory:
    """Factory for creating content extractor provider instances."""

    # Registry of available providers
    _providers = {
        ContentExtractorProvider.TRAFILATURA: TrafilaturaContentExtractor,
        ContentExtractorProvider.BEAUTIFULSOUP: BeautifulSoupContentExtractor,
        # Add more providers here as they're implemented
        # ContentExtractorProvider.READABILITY: ReadabilityContentExtractor,
        # ContentExtractorProvider.NEWSPAPER3K: Newspaper3KContentExtractor,
    }

    # Singleton instances
    _instances: Dict[str, ContentExtractorProviderInterface] = {}

    @classmethod
    def create_provider(
        cls, provider: ContentExtractorProvider, **kwargs: Any
    ) -> ContentExtractorProviderInterface:
        """
        Create a new content extractor provider instance.

        Args:
            provider: Content extractor provider type
            **kwargs: Additional provider-specific configuration

        Returns:
            Content extractor provider instance

        Raises:
            ValueError: If provider is not supported
            Exception: If provider initialization fails
        """
        if provider not in cls._providers:
            raise ValueError(
                f"Unsupported content extractor provider: {provider}"
            )

        provider_class = cls._providers[provider]

        try:
            instance = provider_class(**kwargs)
            logger.info(
                f"Created {provider} content extractor provider instance"
            )
            return instance
        except Exception as e:
            logger.error(
                f"Failed to create {provider} content extractor provider: {str(e)}"
            )
            raise

    @classmethod
    def get_provider(
        cls,
        provider: Optional[ContentExtractorProvider] = None,
        **kwargs: Any,
    ) -> Optional[ContentExtractorProviderInterface]:
        """
        Get or create a content extractor provider instance (singleton pattern).

        Args:
            provider: Content extractor provider type (defaults to configured provider)
            **kwargs: Additional provider-specific configuration

        Returns:
            Content extractor provider instance or None if not configured
        """
        # Determine provider from environment or parameter
        if provider is None:
            provider_name = os.getenv(
                "CONTENT_EXTRACTOR_PROVIDER", "trafilatura"
            ).lower()
            try:
                provider = ContentExtractorProvider(provider_name)
            except ValueError:
                logger.warning(
                    f"Unknown content extractor provider in config: {provider_name}, defaulting to Trafilatura"
                )
                provider = ContentExtractorProvider.TRAFILATURA

        # Check if instance already exists
        provider_key = f"{provider}_{hash(frozenset(kwargs.items()) if kwargs else frozenset())}"
        if provider_key in cls._instances:
            return cls._instances[provider_key]

        try:
            # Create new instance
            instance = cls.create_provider(provider, **kwargs)
            cls._instances[provider_key] = instance
            return instance
        except Exception as e:
            logger.error(
                f"Failed to get {provider} provider: {str(e)}"
            )
            return None

    @classmethod
    def get_fallback_chain(
        cls, **kwargs: Any
    ) -> List[ContentExtractorProviderInterface]:
        """
        Get a chain of content extractor providers for fallback processing.

        Args:
            **kwargs: Additional provider-specific configuration

        Returns:
            List of content extractor providers in fallback order
        """
        providers = []

        # Define fallback order
        fallback_order = [
            ContentExtractorProvider.TRAFILATURA,
            ContentExtractorProvider.BEAUTIFULSOUP,
        ]

        for provider_type in fallback_order:
            try:
                provider = cls.get_provider(provider_type, **kwargs)
                if provider:
                    providers.append(provider)
            except Exception as e:
                logger.warning(
                    f"Failed to create {provider_type} provider for fallback chain: {str(e)}"
                )
                continue

        return providers

    @classmethod
    def get_available_providers(
        cls,
    ) -> list[ContentExtractorProvider]:
        """
        Get list of available content extractor providers.

        Returns:
            List of available provider types
        """
        return list(cls._providers.keys())

    @classmethod
    def is_provider_available(
        cls, provider: ContentExtractorProvider
    ) -> bool:
        """
        Check if a provider is available and configured.

        Args:
            provider: Content extractor provider type to check

        Returns:
            True if provider is available and configured, False otherwise
        """
        if provider not in cls._providers:
            return False

        try:
            # Try to create an instance to test configuration
            test_instance = cls.create_provider(provider)
            return test_instance.is_configured()
        except Exception:
            return False

    @classmethod
    def clear_instances(cls) -> None:
        """Clear all cached provider instances."""
        cls._instances.clear()
        logger.info(
            "Cleared all content extractor provider instances"
        )


# Convenience function for getting the default content extractor provider
def get_content_extractor_provider(
    **kwargs: Any,
) -> Optional[ContentExtractorProviderInterface]:
    """
    Get the default content extractor provider instance.

    Args:
        **kwargs: Additional provider-specific configuration

    Returns:
        Content extractor provider instance or None if not configured
    """
    return ContentExtractorServiceFactory.get_provider(**kwargs)


# Convenience function for getting the fallback chain
def get_content_extractor_fallback_chain(
    **kwargs: Any,
) -> List[ContentExtractorProviderInterface]:
    """
    Get a fallback chain of content extractor providers.

    Args:
        **kwargs: Additional provider-specific configuration

    Returns:
        List of content extractor providers in fallback order
    """
    return ContentExtractorServiceFactory.get_fallback_chain(**kwargs)
