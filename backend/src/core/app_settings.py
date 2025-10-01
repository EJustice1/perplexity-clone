"""
Application Settings - Non-sensitive configuration data.

This module contains application settings that can be safely committed to version control
and used both locally and in production. Sensitive data like API keys should be kept
in environment variables or secret management systems.
"""

import os
from typing import List, Optional, Any
from pydantic import BaseModel, Field, field_validator


class AppSettings(BaseModel):
    """Application settings with validation and defaults."""

    # Application metadata
    app_name: str = "Interactive Search Engine API"
    app_version: str = "0.1.0"
    app_description: str = (
        "Backend API for the Interactive Search Engine project"
    )

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
    log_format: str = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Firestore configuration
    gcp_project_id: str = Field(
        default="",
        description="GCP project ID used for Firestore operations",
    )
    firestore_collection: str = Field(
        default="topic_subscriptions",
        description="Firestore collection name for storing subscriptions",
    )

    # SMTP configuration for Stage 5
    smtp_host: str = Field(default="", description="SMTP host")
    smtp_port: int = Field(default=587, description="SMTP port")
    smtp_username: str = Field(default="", description="SMTP username")
    smtp_password: str = Field(default="", description="SMTP password")
    smtp_from: str = Field(default="", description="SMTP from address")
    smtp_use_tls: bool = Field(default=True, description="Use TLS for SMTP")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> List[str]:
        """Parse CORS origins from environment variable or use default."""
        if isinstance(v, str):
            return [
                origin.strip()
                for origin in v.split(",")
                if origin.strip()
            ]
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
            raise ValueError(
                f"Environment must be one of: {valid_environments}"
            )
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level value."""
        valid_levels = [
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ]
        if v.upper() not in valid_levels:
            raise ValueError(
                f"Log level must be one of: {valid_levels}"
            )
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
            origins.append(
                "https://perplexity-clone-frontend-rg6a7wrdka-uc.a.run.app"
            )

            if lb_url:
                origins.append(lb_url)

        return origins


# Global settings instance
app_settings = AppSettings()


# Override settings from environment variables
def load_settings_from_env() -> None:
    """Load settings from environment variables."""
    # LLM settings
    llm_provider = os.getenv("LLM_PROVIDER")
    if llm_provider:
        app_settings.llm_provider = llm_provider

    llm_model_name = os.getenv("LLM_MODEL_NAME")
    if llm_model_name:
        app_settings.llm_model_name = llm_model_name

    llm_max_tokens = os.getenv("LLM_MAX_TOKENS")
    if llm_max_tokens:
        try:
            app_settings.llm_max_tokens = int(llm_max_tokens)
        except ValueError:
            print(
                f"Warning: Invalid LLM_MAX_TOKENS value: {llm_max_tokens}"
            )

    llm_temperature = os.getenv("LLM_TEMPERATURE")
    if llm_temperature:
        try:
            app_settings.llm_temperature = float(llm_temperature)
        except ValueError:
            print(
                f"Warning: Invalid LLM_TEMPERATURE value: {llm_temperature}"
            )

    # Web search settings
    web_search_provider = os.getenv("WEB_SEARCH_PROVIDER")
    if web_search_provider:
        app_settings.web_search_provider = web_search_provider

    web_search_max_results = os.getenv("WEB_SEARCH_MAX_RESULTS")
    if web_search_max_results:
        try:
            app_settings.web_search_max_results = int(
                web_search_max_results
            )
        except ValueError:
            print(
                f"Warning: Invalid WEB_SEARCH_MAX_RESULTS value: {web_search_max_results}"
            )

    # Content extraction settings
    content_extractor_provider = os.getenv(
        "CONTENT_EXTRACTOR_PROVIDER"
    )
    if content_extractor_provider:
        app_settings.content_extractor_provider = (
            content_extractor_provider
        )

    content_extractor_max_content_length = os.getenv(
        "CONTENT_EXTRACTOR_MAX_CONTENT_LENGTH"
    )
    if content_extractor_max_content_length:
        try:
            app_settings.content_extractor_max_content_length = int(
                content_extractor_max_content_length
            )
        except ValueError:
            print(
                f"Warning: Invalid CONTENT_EXTRACTOR_MAX_CONTENT_LENGTH value: {content_extractor_max_content_length}"
            )

    # Environment
    environment = os.getenv("ENVIRONMENT")
    if environment:
        app_settings.environment = environment

    # CORS origins
    cors_origins_env = os.getenv("CORS_ORIGINS")
    if cors_origins_env:
        app_settings.cors_origins = [
            origin.strip()
            for origin in cors_origins_env.split(",")
            if origin.strip()
        ]

    # Performance settings
    max_concurrent_requests = os.getenv("MAX_CONCURRENT_REQUESTS")
    if max_concurrent_requests:
        try:
            app_settings.max_concurrent_requests = int(
                max_concurrent_requests
            )
        except ValueError:
            print(
                f"Warning: Invalid MAX_CONCURRENT_REQUESTS value: {max_concurrent_requests}"
            )

    # Logging
    log_level = os.getenv("LOG_LEVEL")
    if log_level:
        app_settings.log_level = log_level

    gcp_project_id = os.getenv("GCP_PROJECT_ID")
    if gcp_project_id:
        app_settings.gcp_project_id = gcp_project_id

    firestore_collection = os.getenv("FIRESTORE_COLLECTION")
    if firestore_collection:
        app_settings.firestore_collection = firestore_collection

    smtp_host = os.getenv("SMTP_HOST")
    if smtp_host:
        app_settings.smtp_host = smtp_host

    smtp_port = os.getenv("SMTP_PORT")
    if smtp_port:
        try:
            app_settings.smtp_port = int(smtp_port)
        except ValueError:
            print(f"Warning: Invalid SMTP_PORT value: {smtp_port}")

    smtp_username = os.getenv("SMTP_USERNAME")
    if smtp_username is not None:
        app_settings.smtp_username = smtp_username

    smtp_password = os.getenv("SMTP_PASSWORD")
    if smtp_password is not None:
        app_settings.smtp_password = smtp_password

    smtp_from = os.getenv("SMTP_FROM")
    if smtp_from:
        app_settings.smtp_from = smtp_from

    smtp_use_tls = os.getenv("SMTP_USE_TLS")
    if smtp_use_tls:
        app_settings.smtp_use_tls = smtp_use_tls.lower() != "false"


# Load settings when module is imported
load_settings_from_env()

# Debug logging for configuration
if app_settings.is_development():
    print(f"Environment: {app_settings.environment}")
    print(f"LLM Provider: {app_settings.llm_provider}")
    print(f"LLM Model: {app_settings.llm_model_name}")
    print(f"Web Search Provider: {app_settings.web_search_provider}")
    print(
        f"Content Extractor Provider: {app_settings.content_extractor_provider}"
    )
    print(
        f"CORS Origins configured: {app_settings.get_cors_origins()}"
    )
