"""
Centralized configuration management for the application.
Handles environment variables, validation, and default values.
"""

import os
from typing import List, Any
from pydantic import BaseModel, field_validator


class Settings(BaseModel):
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

    # CORS configuration - Default includes localhost and Cloud Run patterns
    cors_origins: List[str] = [
        "http://localhost:3000",
        "https://localhost:3000",
        # Cloud Run patterns - will be expanded by environment variables
    ]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> List[str]:
        """Parse CORS origins from environment variable or use default."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return v
        else:
            return []


# Global settings instance
settings = Settings()

# Override CORS origins from environment if provided
cors_origins_env = os.getenv("CORS_ORIGINS")
if cors_origins_env:
    settings.cors_origins = [
        origin.strip() for origin in cors_origins_env.split(",") if origin.strip()
    ]

# Add Cloud Run specific origins for production and staging
if os.getenv("ENVIRONMENT") in ["production", "staging"]:
    # Allow Cloud Run domains for the project
    project_id = os.getenv("PROJECT_ID", "perplexity-clone-468820")
    region = os.getenv("REGION", "us-central1")

    # Add Cloud Run domain patterns
    cloud_run_origins = [
        # Allow all Cloud Run services in the region
        f"https://*.{region}.run.app",
        # Allow all services in the project
        f"https://*.{project_id}.run.app",
    ]

    # Add to existing origins
    settings.cors_origins.extend(cloud_run_origins)

# For local development, always add common Cloud Run patterns for testing
if os.getenv("ENVIRONMENT") == "development" or not os.getenv("ENVIRONMENT"):
    # Add Cloud Run patterns for local testing
    cloud_run_test_origins = [
        "https://*.us-central1.run.app",
        "https://*.perplexity-clone-468820.run.app",
    ]

    # Add to existing origins
    settings.cors_origins.extend(cloud_run_test_origins)

# Debug logging for CORS configuration
print(f"CORS Origins configured: {settings.cors_origins}")
