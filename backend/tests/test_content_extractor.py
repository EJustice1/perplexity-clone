"""
Tests for the content extraction service.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.content_extractor import (
    ContentExtractor,
    ContentExtractionResult,
    create_content_extractor,
    get_content_extractor,
)


class TestContentExtractionResult:
    """Test the ContentExtractionResult data structure."""

    def test_content_extraction_result_creation(self):
        """Test creating a ContentExtractionResult instance."""
        result = ContentExtractionResult(
            url="https://example.com",
            title="Test Page",
            extracted_text="This is test content",
            extraction_method="trafilatura",
            success=True,
        )
        
        assert result.url == "https://example.com"
        assert result.title == "Test Page"
        assert result.extracted_text == "This is test content"
        assert result.extraction_method == "trafilatura"
        assert result.success is True
        assert result.error_message is None

    def test_content_extraction_result_with_error(self):
        """Test creating a ContentExtractionResult instance with error."""
        result = ContentExtractionResult(
            url="https://example.com",
            title="",
            extracted_text="",
            extraction_method="failed",
            success=False,
            error_message="Network error",
        )
        
        assert result.success is False
        assert result.error_message == "Network error"

    def test_to_dict_conversion(self):
        """Test converting ContentExtractionResult to dictionary."""
        result = ContentExtractionResult(
            url="https://example.com",
            title="Test Page",
            extracted_text="Test content",
            extraction_method="trafilatura",
            success=True,
        )
        
        result_dict = result.to_dict()
        assert result_dict["url"] == "https://example.com"
        assert result_dict["title"] == "Test Page"
        assert result_dict["extracted_text"] == "Test content"
        assert result_dict["extraction_method"] == "trafilatura"
        assert result_dict["success"] is True


class TestContentExtractor:
    """Test the ContentExtractor service."""

    @pytest.fixture
    def content_extractor(self):
        """Create a ContentExtractor instance for testing."""
        return ContentExtractor(timeout=10.0, max_content_length=1000)

    @pytest.fixture
    def mock_html_content(self):
        """Sample HTML content for testing."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Page Title</title>
        </head>
        <body>
            <h1>Main Heading</h1>
            <main>
                <p>This is the main content of the page.</p>
                <p>It contains multiple paragraphs with useful information.</p>
            </main>
            <nav>Navigation content</nav>
            <footer>Footer content</footer>
        </body>
        </html>
        """

    def test_content_extractor_initialization(self, content_extractor):
        """Test ContentExtractor initialization with custom parameters."""
        assert content_extractor.timeout == 10.0
        assert content_extractor.max_content_length == 1000

    def test_extract_title_from_html(self, content_extractor, mock_html_content):
        """Test extracting title from HTML content."""
        title = content_extractor._extract_title(mock_html_content)
        assert title == "Test Page Title"

    def test_extract_title_fallback_to_h1(self, content_extractor):
        """Test title extraction falls back to h1 when no title tag exists."""
        html_without_title = """
        <html>
        <body>
            <h1>Main Heading</h1>
            <p>Content</p>
        </body>
        </html>
        """
        title = content_extractor._extract_title(html_without_title)
        assert title == "Main Heading"

    def test_extract_title_no_title_or_h1(self, content_extractor):
        """Test title extraction returns empty string when no title or h1 exists."""
        html_without_title = """
        <html>
        <body>
            <p>Content</p>
        </body>
        </html>
        """
        title = content_extractor._extract_title(html_without_title)
        assert title == ""

    @patch('src.services.content_extractor.trafilatura.extract')
    def test_extract_with_trafilatura_success(self, mock_trafilatura, content_extractor, mock_html_content):
        """Test successful content extraction using trafilatura."""
        mock_trafilatura.return_value = "Extracted content from trafilatura that is long enough to pass the threshold"
        
        result = content_extractor._extract_with_trafilatura(mock_html_content)
        
        assert result == "Extracted content from trafilatura that is long enough to pass the threshold"
        mock_trafilatura.assert_called_once_with(mock_html_content, include_formatting=False)

    @patch('src.services.content_extractor.trafilatura.extract')
    def test_extract_with_trafilatura_failure(self, mock_trafilatura, content_extractor, mock_html_content):
        """Test trafilatura extraction failure falls back to BeautifulSoup."""
        mock_trafilatura.return_value = None
        
        result = content_extractor._extract_with_trafilatura(mock_html_content)
        
        assert result is None

    @patch('src.services.content_extractor.BeautifulSoup')
    def test_extract_with_beautifulsoup_success(self, mock_bs4, content_extractor, mock_html_content):
        """Test successful content extraction using BeautifulSoup."""
        mock_soup = MagicMock()
        mock_soup.find.return_value = None  # No main/article/content div
        mock_soup.get_text.return_value = "Extracted content from BeautifulSoup that is long enough to pass the threshold"
        mock_bs4.return_value = mock_soup
        
        result = content_extractor._extract_with_beautifulsoup(mock_html_content)
        
        assert result == "Extracted content from BeautifulSoup that is long enough to pass the threshold"

    @patch('src.services.content_extractor.BeautifulSoup')
    def test_extract_with_beautifulsoup_find_main_content(self, mock_bs4, content_extractor, mock_html_content):
        """Test BeautifulSoup extraction finds main content area."""
        mock_soup = MagicMock()
        mock_main = MagicMock()
        mock_main.get_text.return_value = "Main content area text that is long enough to pass the threshold"
        mock_soup.find.side_effect = lambda tag, **kwargs: mock_main if tag == "main" else None
        
        mock_bs4.return_value = mock_soup
        
        result = content_extractor._extract_with_beautifulsoup(mock_html_content)
        
        assert result == "Main content area text that is long enough to pass the threshold"

    @patch('src.services.content_extractor.httpx.AsyncClient')
    @pytest.mark.asyncio
    async def test_fetch_html_content_success(self, mock_client_class, content_extractor):
        """Test successful HTML content fetching."""
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.text = "<html>Test content</html>"
        mock_response.headers = {"content-type": "text/html"}
        mock_response.raise_for_status = MagicMock()
        
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        result = await content_extractor._fetch_html_content("https://example.com")
        
        assert result == "<html>Test content</html>"

    @patch('src.services.content_extractor.httpx.AsyncClient')
    @pytest.mark.asyncio
    async def test_fetch_html_content_wrong_content_type(self, mock_client_class, content_extractor):
        """Test HTML fetching fails for non-HTML content."""
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = "{}"
        mock_response.raise_for_status = MagicMock()
        
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        result = await content_extractor._fetch_html_content("https://example.com")
        
        assert result is None

    @patch('src.services.content_extractor.httpx.AsyncClient')
    @pytest.mark.asyncio
    async def test_fetch_html_content_http_error(self, mock_client_class, content_extractor):
        """Test HTML fetching handles HTTP errors gracefully."""
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get.side_effect = Exception("HTTP error")
        mock_client_class.return_value = mock_client
        
        result = await content_extractor._fetch_html_content("https://example.com")
        
        assert result is None

    @pytest.mark.asyncio
    async def test_extract_content_from_single_url_success(self, content_extractor, mock_html_content):
        """Test successful content extraction from a single URL."""
        with patch.object(content_extractor, '_fetch_html_content', return_value=mock_html_content), \
             patch.object(content_extractor, '_extract_title', return_value="Test Page Title"), \
             patch.object(content_extractor, '_extract_with_trafilatura', return_value="Extracted content that is long enough"):
            
            result = await content_extractor._extract_content_from_single_url("https://example.com")
            
            assert result.success is True
            assert result.url == "https://example.com"
            assert result.title == "Test Page Title"
            assert result.extracted_text == "Extracted content that is long enough"
            assert result.extraction_method == "trafilatura"

    @pytest.mark.asyncio
    async def test_extract_content_from_single_url_fetch_failure(self, content_extractor):
        """Test content extraction handles fetch failures gracefully."""
        with patch.object(content_extractor, '_fetch_html_content', return_value=None):
            result = await content_extractor._extract_content_from_single_url("https://example.com")
            
            assert result.success is False
            assert result.error_message == "Failed to fetch HTML content"

    @pytest.mark.asyncio
    async def test_extract_content_from_urls_empty_list(self, content_extractor):
        """Test content extraction from empty URL list."""
        result = await content_extractor.extract_content_from_urls([])
        assert result == []

    @pytest.mark.asyncio
    async def test_extract_content_from_urls_concurrent_processing(self, content_extractor):
        """Test concurrent content extraction from multiple URLs."""
        urls = ["https://example1.com", "https://example2.com"]
        
        with patch.object(content_extractor, '_extract_content_from_single_url') as mock_extract:
            mock_extract.return_value = ContentExtractionResult(
                url="https://example.com",
                title="Test",
                extracted_text="Content",
                extraction_method="trafilatura",
                success=True,
            )
            
            result = await content_extractor.extract_content_from_urls(urls, max_concurrent=2)
            
            assert len(result) == 2
            assert mock_extract.call_count == 2


class TestContentExtractorFactory:
    """Test the content extractor factory functions."""

    def test_create_content_extractor(self):
        """Test creating a content extractor with default settings."""
        extractor = create_content_extractor()
        
        assert isinstance(extractor, ContentExtractor)
        assert extractor.timeout == 30.0
        assert extractor.max_content_length == 50000

    def test_get_content_extractor_singleton(self):
        """Test that get_content_extractor returns the same instance."""
        extractor1 = get_content_extractor()
        extractor2 = get_content_extractor()
        
        assert extractor1 is extractor2
        assert isinstance(extractor1, ContentExtractor)
