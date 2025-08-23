"""
Content Extractor Provider Interface - Defines the contract for all content extraction implementations.

This interface allows for easy switching between different content extraction methods
(Trafilatura, BeautifulSoup, Readability, etc.) without changing the core business logic.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ContentExtractorProvider(str, Enum):
    """Supported content extractor providers."""
    TRAFILATURA = "trafilatura"
    BEAUTIFULSOUP = "beautifulsoup"
    READABILITY = "readability"
    NEWSPAPER3K = "newspaper3k"


@dataclass
class ContentExtractionRequest:
    """Request object for content extraction operations."""
    url: str
    html_content: Optional[str] = None  # Pre-fetched HTML content
    extract_comments: bool = False
    include_links: bool = False
    include_images: bool = False
    language: Optional[str] = None


@dataclass
class ContentExtractionResult:
    """Individual content extraction result."""
    url: str
    title: str
    extracted_text: str
    extraction_method: str
    success: bool
    error_message: Optional[str] = None
    author: Optional[str] = None
    publish_date: Optional[str] = None
    language: Optional[str] = None
    word_count: Optional[int] = None
    reading_time: Optional[int] = None  # in minutes


@dataclass
class ContentExtractionResponse:
    """Response object from content extraction operations."""
    results: List[ContentExtractionResult]
    success: bool
    extraction_time: Optional[float] = None
    error_message: Optional[str] = None
    provider: Optional[str] = None
    total_processed: Optional[int] = None
    successful_extractions: Optional[int] = None


class ContentExtractorProviderInterface(ABC):
    """
    Abstract base class for all content extractor providers.
    
    All content extraction implementations must inherit from this class and implement
    the required methods to ensure consistent behavior across providers.
    """

    @abstractmethod
    def __init__(self, **kwargs):
        """
        Initialize the content extractor provider.
        
        Args:
            **kwargs: Provider-specific configuration options
        """
        pass

    @abstractmethod
    async def extract_content(self, request: ContentExtractionRequest) -> ContentExtractionResult:
        """
        Extract content from a single URL or HTML.
        
        Args:
            request: Content extraction request
            
        Returns:
            ContentExtractionResult containing extracted content and metadata
        """
        pass

    @abstractmethod
    async def extract_content_batch(self, requests: List[ContentExtractionRequest]) -> ContentExtractionResponse:
        """
        Extract content from multiple URLs or HTML documents.
        
        Args:
            requests: List of content extraction requests
            
        Returns:
            ContentExtractionResponse containing all results and metadata
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
    def get_supported_content_types(self) -> List[str]:
        """
        Get list of content types supported by this provider.
        
        Returns:
            List of supported content types (html, pdf, etc.)
        """
        pass

    @abstractmethod
    def validate_content_type(self, content_type: str) -> bool:
        """
        Validate if a content type is supported by this provider.
        
        Args:
            content_type: Content type to validate
            
        Returns:
            True if content type is supported, False otherwise
        """
        pass
