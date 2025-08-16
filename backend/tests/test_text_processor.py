"""
Unit tests for the search service.
"""

import pytest
import sys
from pathlib import Path

# Add the src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.text_processor import search_service


class TestSearchService:
    """Test cases for SearchService."""

    def test_search_success(self):
        """Test successful search processing."""
        result = search_service.search("Hello World")
        assert result == "You searched for: Hello World"

    def test_search_with_whitespace(self):
        """Test search with leading/trailing whitespace."""
        result = search_service.search("  Hello World  ")
        assert result == "You searched for: Hello World"

    def test_search_empty_string(self):
        """Test search with empty string."""
        with pytest.raises(ValueError, match="Search query cannot be empty"):
            search_service.search("")

    def test_search_whitespace_only(self):
        """Test search with whitespace-only string."""
        with pytest.raises(ValueError, match="Search query cannot be empty"):
            search_service.search("   ")

    def test_search_none(self):
        """Test search with None value."""
        with pytest.raises(ValueError, match="Search query cannot be empty"):
            search_service.search(None)

    def test_validate_query_success(self):
        """Test successful query validation."""
        assert search_service.validate_query("Hello World") is True
        assert search_service.validate_query("  Hello World  ") is True

    def test_validate_query_failure(self):
        """Test failed query validation."""
        assert search_service.validate_query("") is False
        assert search_service.validate_query("   ") is False
        assert search_service.validate_query(None) is False

    def test_search_with_special_characters(self):
        """Test search with special characters and numbers."""
        result = search_service.search("What is 2+2? & AI/ML")
        assert result == "You searched for: What is 2+2? & AI/ML"

    def test_search_with_long_query(self):
        """Test search with a longer query."""
        long_query = "This is a very long search query that tests the system's ability to handle extended text input without any issues or problems"
        result = search_service.search(long_query)
        assert result == f"You searched for: {long_query}"

    def test_search_with_unicode(self):
        """Test search with unicode characters."""
        result = search_service.search("Hello 世界 🌍")
        assert result == "You searched for: Hello 世界 🌍"
