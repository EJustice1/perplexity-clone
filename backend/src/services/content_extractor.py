"""
Content extraction service layer.
Contains business logic for extracting and cleaning textual content from web pages.
"""

import asyncio
import logging
from typing import List, Optional
import httpx
import trafilatura
from bs4 import BeautifulSoup
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ContentExtractionResult:
    """Data structure for content extraction results."""

    def __init__(
        self,
        url: str,
        title: str,
        extracted_text: str,
        extraction_method: str,
        success: bool,
        error_message: Optional[str] = None,
    ):
        self.url = url
        self.title = title
        self.extracted_text = extracted_text
        self.extraction_method = extraction_method
        self.success = success
        self.error_message = error_message

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "url": self.url,
            "title": self.title,
            "extracted_text": self.extracted_text,
            "extraction_method": self.extraction_method,
            "success": self.success,
            "error_message": self.error_message,
        }


class ContentExtractor:
    """Service class for extracting content from web pages."""

    def __init__(self, timeout: float = 30.0, max_content_length: int = 50000):
        self.timeout = timeout
        self.max_content_length = max_content_length

    async def extract_content_from_urls(
        self, urls: List[str], max_concurrent: int = 3
    ) -> List[ContentExtractionResult]:
        """
        Extract content from multiple URLs concurrently.

        Args:
            urls: List of URLs to extract content from
            max_concurrent: Maximum number of concurrent requests

        Returns:
            List of ContentExtractionResult objects
        """
        if not urls:
            return []

        # Limit concurrent requests to avoid overwhelming servers
        semaphore = asyncio.Semaphore(max_concurrent)
        
        tasks = [
            self._extract_content_with_semaphore(semaphore, url) 
            for url in urls
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and return valid results
        valid_results = []
        for result in results:
            if isinstance(result, ContentExtractionResult):
                valid_results.append(result)
            else:
                logger.error(f"Content extraction failed with exception: {result}")
        
        return valid_results

    async def _extract_content_with_semaphore(
        self, semaphore: asyncio.Semaphore, url: str
    ) -> ContentExtractionResult:
        """Extract content from a single URL using a semaphore for concurrency control."""
        async with semaphore:
            return await self._extract_content_from_single_url(url)

    async def _extract_content_from_single_url(self, url: str) -> ContentExtractionResult:
        """
        Extract content from a single URL.

        Args:
            url: The URL to extract content from

        Returns:
            ContentExtractionResult object
        """
        try:
            logger.info(f"Extracting content from: {url}")
            
            # Fetch HTML content
            html_content = await self._fetch_html_content(url)
            if not html_content:
                return ContentExtractionResult(
                    url=url,
                    title="",
                    extracted_text="",
                    extraction_method="failed",
                    success=False,
                    error_message="Failed to fetch HTML content",
                )

            # Extract title
            title = self._extract_title(html_content)
            
            # Extract main content using trafilatura (primary method)
            extracted_text = self._extract_with_trafilatura(html_content)
            
            if extracted_text:
                # Truncate if too long
                if len(extracted_text) > self.max_content_length:
                    extracted_text = extracted_text[:self.max_content_length] + "..."
                
                logger.info(f"Successfully extracted {len(extracted_text)} characters from {url}")
                return ContentExtractionResult(
                    url=url,
                    title=title,
                    extracted_text=extracted_text,
                    extraction_method="trafilatura",
                    success=True,
                )
            
            # Fallback to BeautifulSoup if trafilatura fails
            extracted_text = self._extract_with_beautifulsoup(html_content)
            if extracted_text:
                if len(extracted_text) > self.max_content_length:
                    extracted_text = extracted_text[:self.max_content_length] + "..."
                
                logger.info(f"Extracted content using BeautifulSoup fallback from {url}")
                return ContentExtractionResult(
                    url=url,
                    title=title,
                    extracted_text=extracted_text,
                    extraction_method="beautifulsoup",
                    success=True,
                )
            
            return ContentExtractionResult(
                url=url,
                title=title,
                extracted_text="",
                extraction_method="failed",
                success=False,
                error_message="No content could be extracted",
            )

        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            return ContentExtractionResult(
                url=url,
                title="",
                extracted_text="",
                extraction_method="failed",
                success=False,
                error_message=str(e),
            )

    async def _fetch_html_content(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from a URL.

        Args:
            url: The URL to fetch

        Returns:
            HTML content as string, or None if failed
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    follow_redirects=True,
                )
                response.raise_for_status()
                
                # Check content type
                content_type = response.headers.get("content-type", "")
                if isinstance(content_type, str) and "text/html" not in content_type.lower():
                    logger.warning(f"Content type is not HTML: {content_type} for {url}")
                    return None
                
                return response.text
                
        except httpx.HTTPStatusError as e:
            logger.warning(f"HTTP error fetching {url}: {e.response.status_code}")
            return None
        except httpx.RequestError as e:
            logger.warning(f"Request error fetching {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {str(e)}")
            return None

    def _extract_title(self, html_content: str) -> str:
        """
        Extract title from HTML content.

        Args:
            html_content: HTML content as string

        Returns:
            Extracted title, or empty string if not found
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            title_tag = soup.find("title")
            if title_tag:
                return title_tag.get_text().strip()
            
            # Fallback to h1 if no title tag
            h1_tag = soup.find("h1")
            if h1_tag:
                return h1_tag.get_text().strip()
            
            return ""
        except Exception as e:
            logger.warning(f"Error extracting title: {str(e)}")
            return ""

    def _extract_with_trafilatura(self, html_content: str) -> Optional[str]:
        """
        Extract content using trafilatura (primary method).

        Args:
            html_content: HTML content as string

        Returns:
            Extracted text, or None if failed
        """
        try:
            extracted = trafilatura.extract(html_content, include_formatting=False)
            if extracted and len(extracted.strip()) > 50:  # Lower threshold for testing
                return extracted.strip()
            return None
        except Exception as e:
            logger.warning(f"Trafilatura extraction failed: {str(e)}")
            return None

    def _extract_with_beautifulsoup(self, html_content: str) -> Optional[str]:
        """
        Extract content using BeautifulSoup (fallback method).

        Args:
            html_content: HTML content as string

        Returns:
            Extracted text, or None if failed
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()
            
            # Try to find main content area
            main_content = soup.find("main") or soup.find("article") or soup.find("div", class_="content")
            
            if main_content:
                text = main_content.get_text(separator=" ", strip=True)
            else:
                # Fallback to body text
                text = soup.get_text(separator=" ", strip=True)
            
            # Clean up whitespace
            text = " ".join(text.split())
            
            if text and len(text) > 50:  # Lower threshold for testing
                return text
            
            return None
        except Exception as e:
            logger.warning(f"BeautifulSoup extraction failed: {str(e)}")
            return None


# Factory function to create the content extractor service
def create_content_extractor() -> ContentExtractor:
    """Create and configure the content extractor service."""
    return ContentExtractor(
        timeout=30.0,
        max_content_length=50000
    )


# Global service instance
content_extractor: Optional[ContentExtractor] = None


def get_content_extractor() -> ContentExtractor:
    """Get the global content extractor instance, creating it if necessary."""
    global content_extractor
    
    if content_extractor is None:
        content_extractor = create_content_extractor()
    
    return content_extractor
