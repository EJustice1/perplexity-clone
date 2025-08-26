"""
Query Enhancement Service - Standalone service for improving search queries.

This service uses an ultra-lightweight LLM to enhance user search queries
before they are processed by the main search pipeline.
"""

import logging
from typing import Optional
from .interfaces.query_enhancement_interface import (
    QueryEnhancementInterface,
    QueryEnhancementRequest,
    QueryEnhancementResponse,
)
from .providers.gemini_2_0_flash_lite_provider import (
    Gemini2FlashLiteProvider,
)

logger = logging.getLogger(__name__)


class QueryEnhancementService:
    """
    Standalone service for query enhancement.

    This service is designed to be simple and lightweight,
    with no factory pattern - direct instantiation only.
    """

    def __init__(self):
        """Initialize the query enhancement service."""
        self.provider: Optional[QueryEnhancementInterface] = None
        self._initialize_provider()

    def _initialize_provider(self) -> None:
        """Initialize the LLM provider for query enhancement."""
        try:
            import os

            api_key = os.getenv("GOOGLE_AI_API_KEY")
            if api_key:
                self.provider = Gemini2FlashLiteProvider(api_key)
                logger.info(
                    "Query enhancement provider initialized successfully"
                )
            else:
                logger.warning(
                    "No GOOGLE_AI_API_KEY environment variable found, query enhancement disabled"
                )
        except Exception as e:
            logger.error(
                f"Failed to initialize query enhancement provider: {str(e)}"
            )

    async def enhance_query(
        self, original_query: str
    ) -> QueryEnhancementResponse:
        """
        Enhance a search query using the ultra-lightweight LLM.

        Args:
            original_query: The user's original search query

        Returns:
            QueryEnhancementResponse with enhanced query or fallback
        """
        if not self.provider or not self.provider.is_configured():
            logger.warning(
                "Query enhancement provider not available, "
                "returning original query"
            )
            return QueryEnhancementResponse(
                enhanced_query=original_query,
                success=False,
                error_message="Enhancement provider not configured",
            )

        if not original_query or not original_query.strip():
            logger.warning("Empty query received, cannot enhance")
            return QueryEnhancementResponse(
                enhanced_query=original_query,
                success=False,
                error_message="Cannot enhance empty query",
            )

        try:
            # Create enhancement request
            request = QueryEnhancementRequest(
                original_query=original_query.strip(),
                max_response_tokens=30,  # Very low limit for speed/cost
            )

            # Enhance query
            response = await self.provider.enhance_query(request)

            if response.success:
                logger.info(
                    f"Query enhanced successfully: "
                    f"'{original_query}' -> '{response.enhanced_query}'"
                )
            else:
                logger.warning(
                    f"Query enhancement failed: {response.error_message}"
                )

            return response

        except Exception as e:
            logger.error(f"Error in query enhancement: {str(e)}")
            return QueryEnhancementResponse(
                enhanced_query=original_query,
                success=False,
                error_message=f"Enhancement error: {str(e)}",
            )

    def is_configured(self) -> bool:
        """Check if the enhancement service is properly configured."""
        return bool(self.provider and self.provider.is_configured())

    def get_provider_name(self) -> str:
        """Get the name of the current enhancement provider."""
        if self.provider:
            return self.provider.get_provider_name()
        return "none"


# Global service instance
_query_enhancement_service: Optional[QueryEnhancementService] = None


def create_query_enhancement_service() -> QueryEnhancementService:
    """Create and configure the query enhancement service."""
    return QueryEnhancementService()


def get_query_enhancement_service() -> QueryEnhancementService:
    """Get the global query enhancement service instance, creating it if necessary."""
    global _query_enhancement_service

    if _query_enhancement_service is None:
        _query_enhancement_service = (
            create_query_enhancement_service()
        )

    return _query_enhancement_service
