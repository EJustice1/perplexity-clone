"""
Service provider implementations for external API integrations.
This module contains concrete implementations of the service interfaces.
"""

from .gemini_2_0_flash_provider import GeminiLLMProvider
from .trafilatura_provider import TrafilaturaContentExtractor
from .beautifulsoup4_provider import BeautifulSoupContentExtractor
from .gemini_2_0_flash_lite_provider import Gemini2FlashLiteProvider  # NEW

__all__ = [
    "GeminiLLMProvider",
    "TrafilaturaContentExtractor",
    "BeautifulSoupContentExtractor",
    "Gemini2FlashLiteProvider",  # NEW
]
