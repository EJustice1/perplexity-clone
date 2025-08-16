"""
Centralized configuration management for the application.
Handles environment variables, validation, and default values.
"""

import os
from typing import List, Any, Optional
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

    # Web search configuration
    serper_api_key: Optional[str] = None

    # CORS configuration - Simplified for GCP deployment
    cors_origins: List[str] = [
        "http://localhost:3000",
        "https://localhost:3000",
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

# Load Serper API key from environment
serper_api_key_env = os.getenv("SERPER_API_KEY")
if serper_api_key_env:
    settings.serper_api_key = serper_api_key_env

# Override CORS origins from environment if provided
cors_origins_env = os.getenv("CORS_ORIGINS")
if cors_origins_env:
    settings.cors_origins = [
        origin.strip() for origin in cors_origins_env.split(",") if origin.strip()
    ]

# Add environment-specific origins
if os.getenv("ENVIRONMENT") in ["production", "staging"]:
    # In production, allow the frontend service domain
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url:
        settings.cors_origins.append(frontend_url)
    
    # Also allow the load balancer domain for flexibility
    lb_url = os.getenv("LOAD_BALANCER_URL")
    if lb_url:
        settings.cors_origins.append(lb_url)
    
    # Add new GCP Cloud Run URL patterns for flexibility
    # New format: *.a.run.app (random hash)
    settings.cors_origins.extend([
        "https://*.a.run.app",
        "https://*.us-central1.run.app"
    ])

# Debug logging for CORS configuration
print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
print(f"Project ID: {os.getenv('PROJECT_ID', 'not set')}")
print(f"Region: {os.getenv('REGION', 'not set')}")
print(f"Frontend URL: {os.getenv('FRONTEND_URL', 'not set')}")
print(f"Load Balancer URL: {os.getenv('LOAD_BALANCER_URL', 'not set')}")
print(f"CORS Origins configured: {settings.cors_origins}")
