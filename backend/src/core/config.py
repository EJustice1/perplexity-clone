"""
Sensitive configuration management for the application.

This module handles only sensitive data like API keys.
Non-sensitive configuration is handled by app_settings.py.
"""

import os
from typing import Optional
from pydantic import BaseModel


class SensitiveSettings(BaseModel):
    """Sensitive application settings that should not be committed to version control."""

    # Web search configuration
    serper_api_key: Optional[str] = None

    # LLM configuration - Only Google Gemini is supported
    google_ai_api_key: Optional[str] = None

    # LangChain-specific environment variables
    gemini_api_key: Optional[str] = None


# Global sensitive settings instance
sensitive_settings = SensitiveSettings()

# Load Serper API key from environment
serper_api_key_env = os.getenv("SERPER_API_KEY")
if serper_api_key_env:
    sensitive_settings.serper_api_key = serper_api_key_env

# Load Google AI API key from environment
google_ai_api_key_env = os.getenv("GOOGLE_AI_API_KEY")
if google_ai_api_key_env:
    sensitive_settings.google_ai_api_key = google_ai_api_key_env

# Load Gemini API key alias for LangChain integrations
gemini_api_key_env = os.getenv("GEMINI_API_KEY")
if gemini_api_key_env:
    sensitive_settings.gemini_api_key = gemini_api_key_env

# Debug logging for sensitive configuration
print(
    f"Serper API Key configured: {'Yes' if sensitive_settings.serper_api_key else 'No'}"
)
print(
    f"Google AI API Key configured: {'Yes' if sensitive_settings.google_ai_api_key else 'No'}"
)
print(
    f"Gemini API Key configured: {'Yes' if sensitive_settings.gemini_api_key else 'No'}"
)
