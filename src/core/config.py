"""
Centralized configuration management for the Perplexity Clone application.
This module provides environment-based configuration for all services.
"""

import os
from typing import Optional

class Config:
    """Base configuration class with common settings."""
    
    # Service identification
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "unknown")
    
    # API configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Frontend configuration
    FRONTEND_HOST: str = os.getenv("FRONTEND_HOST", "0.0.0.0")
    FRONTEND_PORT: int = int(os.getenv("FRONTEND_PORT", "5001"))
    
    # Environment and debugging
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Middleware configuration
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "true").lower() == "true"
    
    # Metrics and health endpoints
    METRICS_PATH: str = os.getenv("METRICS_PATH", "/metrics")
    HEALTH_PATH: str = os.getenv("HEALTH_PATH", "/health")
    
    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # CORS configuration
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Future middleware configuration can be added here:
    # - Authentication settings (JWT keys, algorithms, expiry)
    # - Caching settings (Redis connection, TTL, eviction policies)
    # - Rate limiting settings (limits, windows, blocking duration)
    # - Security settings (CORS, CSP, rate limiting)
    # - Logging settings (structured logging, correlation IDs)
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return cls.ENVIRONMENT.lower() == "production"
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment."""
        return cls.ENVIRONMENT.lower() == "development"
    
    @classmethod
    def get_api_url(cls) -> str:
        """Get the full API URL."""
        return f"http://{cls.API_HOST}:{cls.API_PORT}"
    
    @classmethod
    def get_frontend_url(cls) -> str:
        """Get the full frontend URL."""
        return f"http://{cls.FRONTEND_HOST}:{cls.FRONTEND_PORT}"

class BackendConfig(Config):
    """Backend-specific configuration."""
    
    SERVICE_NAME: str = "backend"
    
    # Uvicorn configuration
    UVICWORKERS: int = int(os.getenv("UVICORN_WORKERS", "1"))
    RELOAD: bool = os.getenv("RELOAD", "false").lower() == "true"
    
    # Future backend-specific middleware settings can be added here:
    # - Authentication configuration
    # - Caching configuration  
    # - Rate limiting configuration
    # - Security configuration

class FrontendConfig(Config):
    """Frontend-specific configuration."""
    
    SERVICE_NAME: str = "frontend"
    
    # Flask-specific settings
    TEMPLATES_AUTO_RELOAD: bool = os.getenv("TEMPLATES_AUTO_RELOAD", "true").lower() == "true"
    
    # Future frontend-specific middleware settings can be added here:
    # - Authentication configuration
    # - Caching configuration
    # - Rate limiting configuration
    # - Security configuration

# Create configuration instances
backend_config = BackendConfig()
frontend_config = FrontendConfig()
