"""
Web Search Service Factory - Creates and manages web search provider instances.

This factory handles the creation of different web search providers based on configuration,
providing a single interface for web search service instantiation.
"""

import logging
import os
from typing import Optional, Dict, Any

from ..interfaces.web_search_interface import WebSearchProviderInterface, WebSearchProvider
# from ..providers.serper_web_search_provider import SerperWebSearchProvider  # TODO: Import when created

logger = logging.getLogger(__name__)


class WebSearchServiceFactory:
    """Factory for creating web search provider instances."""
    
    # Registry of available providers
    _providers = {
        # WebSearchProvider.SERPER: SerperWebSearchProvider,  # TODO: Add when created
        # Add more providers here as they're implemented
        # WebSearchProvider.GOOGLE_CUSTOM_SEARCH: GoogleCustomSearchProvider,
        # WebSearchProvider.BING_SEARCH: BingSearchProvider,
        # WebSearchProvider.BRAVE_SEARCH: BraveSearchProvider,
    }
    
    # Singleton instances
    _instances: Dict[str, WebSearchProviderInterface] = {}

    @classmethod
    def create_provider(
        self, 
        provider: WebSearchProvider, 
        api_key: str,
        **kwargs
    ) -> WebSearchProviderInterface:
        """
        Create a new web search provider instance.
        
        Args:
            provider: Web search provider type
            api_key: API key for the provider
            **kwargs: Additional provider-specific configuration
            
        Returns:
            Web search provider instance
            
        Raises:
            ValueError: If provider is not supported
            Exception: If provider initialization fails
        """
        if provider not in self._providers:
            raise ValueError(f"Unsupported web search provider: {provider}")
        
        provider_class = self._providers[provider]
        
        try:
            instance = provider_class(api_key=api_key, **kwargs)
            logger.info(f"Created {provider} web search provider instance")
            return instance
        except Exception as e:
            logger.error(f"Failed to create {provider} web search provider: {str(e)}")
            raise

    @classmethod
    def get_provider(
        self, 
        provider: Optional[WebSearchProvider] = None,
        **kwargs
    ) -> Optional[WebSearchProviderInterface]:
        """
        Get or create a web search provider instance (singleton pattern).
        
        Args:
            provider: Web search provider type (defaults to configured provider)
            **kwargs: Additional provider-specific configuration
            
        Returns:
            Web search provider instance or None if not configured
        """
        # Determine provider from environment or parameter
        if provider is None:
            provider_name = os.getenv("WEB_SEARCH_PROVIDER", "serper").lower()
            try:
                provider = WebSearchProvider(provider_name)
            except ValueError:
                logger.warning(f"Unknown web search provider in config: {provider_name}, defaulting to Serper")
                provider = WebSearchProvider.SERPER

        # Check if instance already exists
        provider_key = f"{provider}_{hash(frozenset(kwargs.items()) if kwargs else frozenset())}"
        if provider_key in self._instances:
            return self._instances[provider_key]

        # Get API key from environment
        api_key = self._get_api_key_for_provider(provider)
        if not api_key:
            logger.warning(f"No API key found for {provider} provider")
            return None

        try:
            # Create new instance
            instance = self.create_provider(provider, api_key, **kwargs)
            self._instances[provider_key] = instance
            return instance
        except Exception as e:
            logger.error(f"Failed to get {provider} provider: {str(e)}")
            return None

    @classmethod
    def _get_api_key_for_provider(self, provider: WebSearchProvider) -> Optional[str]:
        """
        Get API key for a specific provider from environment variables.
        
        Args:
            provider: Web search provider type
            
        Returns:
            API key string or None if not found
        """
        key_mapping = {
            WebSearchProvider.SERPER: "SERPER_API_KEY",
            WebSearchProvider.GOOGLE_CUSTOM_SEARCH: "GOOGLE_CUSTOM_SEARCH_API_KEY",
            WebSearchProvider.BING_SEARCH: "BING_SEARCH_API_KEY",
            WebSearchProvider.BRAVE_SEARCH: "BRAVE_SEARCH_API_KEY",
        }
        
        provider_key = key_mapping.get(provider)
        if provider_key:
            return os.getenv(provider_key)
        
        return None

    @classmethod
    def get_available_providers(self) -> list[WebSearchProvider]:
        """
        Get list of available web search providers.
        
        Returns:
            List of available provider types
        """
        return list(self._providers.keys())

    @classmethod
    def is_provider_available(self, provider: WebSearchProvider) -> bool:
        """
        Check if a provider is available and configured.
        
        Args:
            provider: Web search provider type to check
            
        Returns:
            True if provider is available and has API key, False otherwise
        """
        if provider not in self._providers:
            return False
        
        api_key = self._get_api_key_for_provider(provider)
        return bool(api_key)

    @classmethod
    def clear_instances(self):
        """Clear all cached provider instances."""
        self._instances.clear()
        logger.info("Cleared all web search provider instances")


# Convenience function for getting the default web search provider
def get_web_search_provider(**kwargs) -> Optional[WebSearchProviderInterface]:
    """
    Get the default web search provider instance.
    
    Args:
        **kwargs: Additional provider-specific configuration
        
    Returns:
        Web search provider instance or None if not configured
    """
    return WebSearchServiceFactory.get_provider(**kwargs)
