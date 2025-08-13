"""
Centralized configuration management for the application.
Handles environment variables, validation, and default values.
"""

import os
from typing import List
from pydantic import BaseModel, validator


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
    
    # CORS configuration
    cors_origins: List[str] = ["http://localhost:3000"]
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from environment variable or use default."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


# Global settings instance
settings = Settings()

# Override CORS origins from environment if provided
if os.getenv("CORS_ORIGINS"):
    settings.cors_origins = [
        origin.strip() 
        for origin in os.getenv("CORS_ORIGINS").split(",") 
        if origin.strip()
    ]
