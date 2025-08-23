"""
Application Settings - Non-sensitive configuration data.

This module contains application settings that can be safely committed to version control
and used both locally and in production. Sensitive data like API keys should be kept
in environment variables or secret management systems.
"""

import os
from typing import List, Optional
from pydantic import BaseModel, field_validator


class AppSettings(BaseModel):
    """Application settings with validation and defaults."""

    # Application metadata
    app_name: str = "Interactive Search Engine API"
    app_version: str = "0.1.0"
    app_description: str = "Backend API for the Interactive Search Engine project"

    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # Environment
    environment: str = "development"

    # LLM Configuration (non-sensitive)
    llm_provider: str = "gemini"
    llm_model_name: str = "gemini-2.0-flash"
    llm_max_tokens: int = 2048
    llm_temperature: float = 0.7

    # Web Search Configuration (non-sensitive)
    web_search_provider: str = "serper"
    web_search_max_results: int = 5
    web_search_timeout: int = 30

    # Content Extraction Configuration (non-sensitive)
    content_extractor_provider: str = "trafilatura"
    content_extractor_max_content_length: int = 50000
    content_extractor_timeout: int = 30
    content_extractor_max_concurrent: int = 2

    # CORS configuration - Simplified for GCP deployment
    cors_origins: List[str] = [
        "http://localhost:3000",
        "https://localhost:3000",
    ]

    # Performance settings
    max_concurrent_requests: int = 10
    request_timeout: int = 60
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour

    # Logging configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: any) -> List[str]:
        """Parse CORS origins from environment variable or use default."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return v
        else:
            return []

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        valid_environments = ["development", "staging", "production"]
        if v not in valid_environments:
            raise ValueError(f"Environment must be one of: {valid_environments}")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level value."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"

    def get_cors_origins(self) -> List[str]:
        """Get CORS origins with environment-specific additions."""
        origins = self.cors_origins.copy()
        
        if self.is_production():
            # Add production-specific origins
            frontend_url = os.getenv("FRONTEND_URL")
            if frontend_url:
                origins.append(frontend_url)
            
            lb_url = os.getenv("LOAD_BALANCER_URL")
            if lb_url:
                origins.append(lb_url)
            
            # Add specific Cloud Run URLs for CORS
            if frontend_url:
                origins.append(frontend_url)
            
            # Add the specific frontend URL from the test output
            origins.append("https://perplexity-clone-frontend-rg6a7wrdka-uc.a.run.app")
            
            if lb_url:
                origins.append(lb_url)
        
        return origins


# Global settings instance
app_settings = AppSettings()

# Override settings from environment variables
def load_settings_from_env():
    """Load settings from environment variables."""
    # LLM settings
    if os.getenv("LLM_PROVIDER"):
        app_settings.llm_provider = os.getenv("LLM_PROVIDER")
    
    if os.getenv("LLM_MODEL_NAME"):
        app_settings.llm_model_name = os.getenv("LLM_MODEL_NAME")
    
    if os.getenv("LLM_MAX_TOKENS"):
        try:
            app_settings.llm_max_tokens = int(os.getenv("LLM_MAX_TOKENS"))
        except ValueError:
            print(f"Warning: Invalid LLM_MAX_TOKENS value: {os.getenv('LLM_MAX_TOKENS')}")
    
    if os.getenv("LLM_TEMPERATURE"):
        try:
            app_settings.llm_temperature = float(os.getenv("LLM_TEMPERATURE"))
        except ValueError:
            print(f"Warning: Invalid LLM_TEMPERATURE value: {os.getenv('LLM_TEMPERATURE')}")

    # Web search settings
    if os.getenv("WEB_SEARCH_PROVIDER"):
        app_settings.web_search_provider = os.getenv("WEB_SEARCH_PROVIDER")
    
    if os.getenv("WEB_SEARCH_MAX_RESULTS"):
        try:
            app_settings.web_search_max_results = int(os.getenv("WEB_SEARCH_MAX_RESULTS"))
        except ValueError:
            print(f"Warning: Invalid WEB_SEARCH_MAX_RESULTS value: {os.getenv('WEB_SEARCH_MAX_RESULTS')}")

    # Content extraction settings
    if os.getenv("CONTENT_EXTRACTOR_PROVIDER"):
        app_settings.content_extractor_provider = os.getenv("CONTENT_EXTRACTOR_PROVIDER")
    
    if os.getenv("CONTENT_EXTRACTOR_MAX_CONTENT_LENGTH"):
        try:
            app_settings.content_extractor_max_content_length = int(os.getenv("CONTENT_EXTRACTOR_MAX_CONTENT_LENGTH"))
        except ValueError:
            print(f"Warning: Invalid CONTENT_EXTRACTOR_MAX_CONTENT_LENGTH value: {os.getenv('CONTENT_EXTRACTOR_MAX_CONTENT_LENGTH')}")

    # Environment
    if os.getenv("ENVIRONMENT"):
        app_settings.environment = os.getenv("ENVIRONMENT")

    # CORS origins
    cors_origins_env = os.getenv("CORS_ORIGINS")
    if cors_origins_env:
        app_settings.cors_origins = [
            origin.strip() for origin in cors_origins_env.split(",") if origin.strip()
        ]

    # Performance settings
    if os.getenv("MAX_CONCURRENT_REQUESTS"):
        try:
            app_settings.max_concurrent_requests = int(os.getenv("MAX_CONCURRENT_REQUESTS"))
        except ValueError:
            print(f"Warning: Invalid MAX_CONCURRENT_REQUESTS value: {os.getenv('MAX_CONCURRENT_REQUESTS')}")

    # Logging
    if os.getenv("LOG_LEVEL"):
        app_settings.log_level = os.getenv("LOG_LEVEL")


# Load settings when module is imported
load_settings_from_env()

# Debug logging for configuration
if app_settings.is_development():
    print(f"Environment: {app_settings.environment}")
    print(f"LLM Provider: {app_settings.llm_provider}")
    print(f"LLM Model: {app_settings.llm_model_name}")
    print(f"Web Search Provider: {app_settings.web_search_provider}")
    print(f"Content Extractor Provider: {app_settings.content_extractor_provider}")
    print(f"CORS Origins configured: {app_settings.get_cors_origins()}")
