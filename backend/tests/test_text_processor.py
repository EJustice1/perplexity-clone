"""
Unit tests for the text processor service.
"""

import pytest
import sys
from pathlib import Path

# Add the src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.text_processor import text_processor_service


class TestTextProcessorService:
    """Test cases for TextProcessorService."""
    
    def test_process_text_success(self):
        """Test successful text processing."""
        result = text_processor_service.process_text("Hello World")
        assert result == "!!! Hello World !!!"
        
    def test_process_text_with_whitespace(self):
        """Test text processing with leading/trailing whitespace."""
        result = text_processor_service.process_text("  Hello World  ")
        assert result == "!!! Hello World !!!"
        
    def test_process_text_empty_string(self):
        """Test text processing with empty string."""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            text_processor_service.process_text("")
            
    def test_process_text_whitespace_only(self):
        """Test text processing with whitespace-only string."""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            text_processor_service.process_text("   ")
            
    def test_process_text_none(self):
        """Test text processing with None value."""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            text_processor_service.process_text(None)
            
    def test_validate_text_success(self):
        """Test successful text validation."""
        assert text_processor_service.validate_text("Hello World") is True
        assert text_processor_service.validate_text("  Hello World  ") is True
        
    def test_validate_text_failure(self):
        """Test failed text validation."""
        assert text_processor_service.validate_text("") is False
        assert text_processor_service.validate_text("   ") is False
        assert text_processor_service.validate_text(None) is False
