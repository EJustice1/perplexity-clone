"""
BeautifulSoup Content Extractor Provider Implementation.

This module provides content extraction using BeautifulSoup,
which serves as a fallback method for basic HTML parsing and text extraction.
"""

import logging
import time
import asyncio
from typing import List, Optional, Any
import httpx

from ..interfaces.content_extractor_interface import (
    ContentExtractorProviderInterface,
    ContentExtractionRequest,
    ContentExtractionResult,
    ContentExtractionResponse,
)

logger = logging.getLogger(__name__)


class BeautifulSoupContentExtractor(
    ContentExtractorProviderInterface
):
    """BeautifulSoup4 implementation of the content extractor provider interface."""

    # Supported content types
    SUPPORTED_CONTENT_TYPES = ["text/html", "application/xhtml+xml"]

    REQUEST_TIMEOUT = 30.0
    MAX_CONTENT_LENGTH = 50000  # characters
    USER_AGENT = "Mozilla/5.0 (compatible; SearchEngine/1.0)"

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the BeautifulSoup content extractor provider.

        Args:
            **kwargs: Additional configuration options
        """
        self.timeout = kwargs.get("timeout", self.REQUEST_TIMEOUT)
        self.max_content_length = kwargs.get(
            "max_content_length", self.MAX_CONTENT_LENGTH
        )
        self.user_agent = kwargs.get("user_agent", self.USER_AGENT)

        logger.info(
            "Initialized BeautifulSoup content extractor provider"
        )

    async def extract_content(
        self, request: ContentExtractionRequest
    ) -> ContentExtractionResult:
        """
        Extract content from a single URL or HTML using BeautifulSoup.

        Args:
            request: Content extraction request

        Returns:
            ContentExtractionResult containing extracted content and metadata
        """
        try:
            # Import BeautifulSoup (lazy import)
            from bs4 import BeautifulSoup

            # Get HTML content
            if request.html_content:
                html_content = request.html_content
            else:
                html_content = await self._fetch_html_content(
                    request.url
                )
                if not html_content:
                    return ContentExtractionResult(
                        url=request.url,
                        title="",
                        extracted_text="",
                        extraction_method="beautifulsoup",
                        success=False,
                        error_message="Failed to fetch HTML content",
                    )

            # Extract metadata
            try:
                import trafilatura

                metadata = trafilatura.extract_metadata(html_content)
                extracted_title = (
                    metadata.title
                    if metadata
                    else self._extract_title_from_html(html_content)
                )
                title = extracted_title or ""
            except ImportError:
                # Fallback to HTML parsing if trafilatura not available
                title = (
                    self._extract_title_from_html(html_content) or ""
                )

            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")

            # Remove unwanted elements
            self._remove_unwanted_elements(soup)

            # Extract main content
            extracted_text = self._extract_main_content(soup)

            if not extracted_text:
                return ContentExtractionResult(
                    url=request.url,
                    title=title or "",
                    extracted_text="",
                    extraction_method="beautifulsoup",
                    success=False,
                    error_message="BeautifulSoup failed to extract meaningful content",
                )

            # Truncate content if too long
            if len(extracted_text) > self.max_content_length:
                extracted_text = (
                    extracted_text[: self.max_content_length] + "..."
                )

            # Calculate additional metadata
            word_count = len(extracted_text.split())
            reading_time = max(
                1, word_count // 200
            )  # Assume 200 words per minute

            logger.debug(
                f"BeautifulSoup extraction successful for {request.url}"
            )

            return ContentExtractionResult(
                url=request.url,
                title=title or "",
                extracted_text=extracted_text,
                extraction_method="beautifulsoup",
                success=True,
                word_count=word_count,
                reading_time=reading_time,
            )

        except ImportError:
            logger.error("BeautifulSoup package not installed")
            return ContentExtractionResult(
                url=request.url,
                title="",
                extracted_text="",
                extraction_method="beautifulsoup",
                success=False,
                error_message="BeautifulSoup package not installed",
            )
        except Exception as e:
            logger.error(
                f"BeautifulSoup extraction error for {request.url}: {str(e)}",
                exc_info=True,
            )
            return ContentExtractionResult(
                url=request.url,
                title="",
                extracted_text="",
                extraction_method="beautifulsoup",
                success=False,
                error_message=f"BeautifulSoup extraction error: {str(e)}",
            )

    async def extract_content_batch(
        self, requests: List[ContentExtractionRequest]
    ) -> ContentExtractionResponse:
        """
        Extract content from multiple URLs using BeautifulSoup.

        Args:
            requests: List of content extraction requests

        Returns:
            ContentExtractionResponse containing all results and metadata
        """
        start_time = time.time()

        try:
            # Process requests concurrently
            tasks = [
                self.extract_content(request) for request in requests
            ]
            results = await asyncio.gather(
                *tasks, return_exceptions=True
            )

            # Filter out exceptions and convert to results
            extraction_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    extraction_results.append(
                        ContentExtractionResult(
                            url=requests[i].url,
                            title="",
                            extracted_text="",
                            extraction_method="beautifulsoup",
                            success=False,
                            error_message=f"Batch extraction exception: {str(result)}",
                        )
                    )
                elif isinstance(result, ContentExtractionResult):
                    extraction_results.append(result)
                else:
                    # Handle unexpected result types
                    extraction_results.append(
                        ContentExtractionResult(
                            url=requests[i].url,
                            title="",
                            extracted_text="",
                            extraction_method="beautifulsoup",
                            success=False,
                            error_message=f"Unexpected result type: {type(result)}",
                        )
                    )

            # Calculate metrics
            successful_extractions = sum(
                1 for result in extraction_results if result.success
            )
            extraction_time = time.time() - start_time

            logger.info(
                f"BeautifulSoup batch extraction completed: {successful_extractions}/{len(requests)} successful in {extraction_time:.2f}s"
            )

            return ContentExtractionResponse(
                results=extraction_results,
                success=successful_extractions > 0,
                extraction_time=extraction_time,
                provider="beautifulsoup",
                total_processed=len(requests),
                successful_extractions=successful_extractions,
            )

        except Exception as e:
            logger.error(
                f"BeautifulSoup batch extraction error: {str(e)}",
                exc_info=True,
            )
            return ContentExtractionResponse(
                results=[],
                success=False,
                extraction_time=time.time() - start_time,
                error_message=f"Batch extraction error: {str(e)}",
                provider="beautifulsoup",
                total_processed=len(requests),
                successful_extractions=0,
            )

    async def _fetch_html_content(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from a URL.

        Args:
            url: URL to fetch content from

        Returns:
            HTML content as string, or None if failed
        """
        try:
            headers = {"User-Agent": self.user_agent}

            async with httpx.AsyncClient(
                timeout=self.timeout
            ) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()

                # Check content type
                content_type = response.headers.get(
                    "content-type", ""
                ).lower()
                if not any(
                    ct in content_type
                    for ct in self.SUPPORTED_CONTENT_TYPES
                ):
                    logger.warning(
                        f"Unsupported content type for {url}: {content_type}"
                    )
                    return None

                return response.text

        except Exception as e:
            logger.error(
                f"Failed to fetch HTML content from {url}: {str(e)}"
            )
            return None

    def _remove_unwanted_elements(self, soup: Any) -> None:
        """
        Remove unwanted HTML elements from the soup.

        Args:
            soup: BeautifulSoup object to clean
        """
        # Remove script and style elements
        for element in soup(
            ["script", "style", "nav", "header", "footer", "aside"]
        ):
            element.decompose()

        # Remove elements with common ad/navigation classes
        unwanted_classes = [
            "advertisement",
            "ad",
            "ads",
            "sidebar",
            "navigation",
            "nav",
            "menu",
            "footer",
            "header",
            "social",
            "share",
            "comment",
        ]

        for class_name in unwanted_classes:
            for element in soup.find_all(
                class_=lambda x: x and class_name in x.lower()
            ):
                element.decompose()

    def _extract_title(self, soup: Any) -> str:
        """
        Extract title from HTML soup.

        Args:
            soup: BeautifulSoup object

        Returns:
            Title string or empty string
        """
        # Try title tag first
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            title_text = title_tag.string
            if title_text:
                return title_text.strip()
            return ""

        # Try h1 as fallback
        h1_tag = soup.find("h1")  # type: ignore
        if h1_tag:
            h1_text = h1_tag.get_text()  # type: ignore
            if h1_text:
                return h1_text.strip()
            return ""

        # Try meta title
        meta_title = soup.find("meta", property="og:title")  # type: ignore
        if meta_title and meta_title.get("content"):
            meta_content = meta_title["content"]  # type: ignore
            if meta_content:
                return meta_content.strip()
            return ""

        return ""

    def _extract_title_from_html(self, html_content: str) -> str:
        """
        Extract title from HTML content using BeautifulSoup.

        Args:
            html_content: HTML content as string

        Returns:
            Extracted title or empty string if not found
        """
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html_content, "html.parser")

            # Try title tag first
            title_tag = soup.find("title")  # type: ignore
            if title_tag:
                title_text = title_tag.get_text()  # type: ignore
                if title_text:
                    return title_text.strip()
                return ""

            # Try h1 tag
            h1_tag = soup.find("h1")  # type: ignore
            if h1_tag:
                h1_text = h1_tag.get_text()  # type: ignore
                if h1_text:
                    return h1_text.strip()
                return ""

            # Try meta title
            meta_title = soup.find("meta", property="og:title")  # type: ignore
            if meta_title and meta_title.get("content"):
                meta_content = meta_title["content"]  # type: ignore
                if meta_content:
                    return meta_content.strip()
                return ""

            return ""
        except Exception as e:
            logger.warning(
                f"Error extracting title from HTML: {str(e)}"
            )
            return ""

    def _extract_main_content(self, soup: Any) -> str:
        """
        Extract main content from HTML soup.

        Args:
            soup: BeautifulSoup object

        Returns:
            Extracted text content
        """
        # Try to find main content areas first
        main_selectors = [
            "main",
            "article",
            ".content",
            ".post",
            ".entry",
            ".article-content",
            ".post-content",
            ".entry-content",
        ]

        for selector in main_selectors:
            main_content = soup.select_one(selector)  # type: ignore
            if main_content:
                text = main_content.get_text(separator=" ", strip=True)  # type: ignore
                if (
                    text and len(text) > 100
                ):  # Only use if substantial content
                    clean_text = text.strip()
                    if clean_text:
                        return clean_text
                    return ""

        # Fallback: extract from body
        body = soup.find("body")  # type: ignore
        if body:
            body_text = body.get_text(separator=" ", strip=True)  # type: ignore
            if body_text:
                clean_text = body_text.strip()
                if clean_text:
                    return clean_text
                return ""
            return ""

        # Last resort: entire document
        doc_text = soup.get_text(separator=" ", strip=True)  # type: ignore
        if doc_text:
            clean_text = doc_text.strip()
            if clean_text:
                return clean_text
            return ""
        return ""

    def is_configured(self) -> bool:
        """
        Check if the BeautifulSoup provider is properly configured.

        Returns:
            True (BeautifulSoup doesn't require external configuration)
        """
        try:
            import bs4

            return True
        except ImportError:
            return False

    def get_provider_name(self) -> str:
        """
        Get the name of the provider.

        Returns:
            String identifier for this provider
        """
        return "beautifulsoup"

    def get_supported_content_types(self) -> List[str]:
        """
        Get list of content types supported by BeautifulSoup.

        Returns:
            List of supported content types
        """
        return self.SUPPORTED_CONTENT_TYPES.copy()

    def validate_content_type(self, content_type: str) -> bool:
        """
        Validate if a content type is supported by BeautifulSoup.

        Args:
            content_type: Content type to validate

        Returns:
            True if content type is supported, False otherwise
        """
        return any(
            ct in content_type.lower()
            for ct in self.SUPPORTED_CONTENT_TYPES
        )

