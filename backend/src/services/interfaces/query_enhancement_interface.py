"""
Query Enhancement Interface - Ultra-lightweight LLM interface for query improvement.

This interface defines the minimal contract for query enhancement operations,
focusing on speed, cost-efficiency, and simplicity.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class QueryEnhancementRequest:
    """Minimal request object for query enhancement."""
    original_query: str
    max_response_tokens: int = 30  # Very low token limit


@dataclass
class QueryEnhancementResponse:
    """Minimal response object for query enhancement."""
    enhanced_query: str
    success: bool
    error_message: Optional[str] = None
    tokens_used: Optional[int] = None


class QueryEnhancementInterface(ABC):
    """
    Abstract base class for ultra-lightweight query enhancement.
    
    This interface is designed for minimal overhead and maximum speed.
    """
    
    @abstractmethod
    async def enhance_query(self, request: QueryEnhancementRequest) -> QueryEnhancementResponse:
        """
        Enhance a search query using minimal LLM processing.

        Args:
            request: QueryEnhancementRequest with original query

        Returns:
            QueryEnhancementResponse with enhanced query or error
        """
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        """Check if the enhancement service is ready."""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of the enhancement provider."""
        pass
