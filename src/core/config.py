"""
Centralized configuration management for the Perplexity Clone application.
Provides environment-based configuration for all services with validation.
"""

import os
from typing import List, Optional, Union
from typing_extensions import Literal

class Config:
    """Base configuration class with common settings across all services."""
    
    # Service identification
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "unknown")
    
    # API configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Frontend configuration
    FRONTEND_HOST: str = os.getenv("FRONTEND_HOST", "0.0.0.0")
    FRONTEND_PORT: int = int(os.getenv("FRONTEND_PORT", "3000"))
    
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
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    
    # Configuration for planned middleware features:
    # - Authentication: JWT keys, algorithms, expiry times
    # - Caching: Redis connection, TTL, eviction policies
    # - Rate limiting: request limits, time windows, blocking duration
    # - Security: CORS policies, CSP headers, rate limiting rules
    # - Logging: structured logging, correlation IDs, log aggregation
    
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
        """Get the full API URL for external service communication."""
        return f"http://{cls.API_HOST}:{cls.API_PORT}"
    
    @classmethod
    def get_frontend_url(cls) -> str:
        """Get the full frontend URL for external service communication."""
        return f"http://{cls.FRONTEND_HOST}:{cls.FRONTEND_PORT}"
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration values and return success status."""
        try:
            # Validate ports are in valid range
            if not (1024 <= cls.API_PORT <= 65535):
                raise ValueError(f"API_PORT {cls.API_PORT} must be between 1024 and 65535")
            if not (1024 <= cls.FRONTEND_PORT <= 65535):
                raise ValueError(f"FRONTEND_PORT {cls.FRONTEND_PORT} must be between 1024 and 65535")
            
            # Validate environment
            if cls.ENVIRONMENT not in ["development", "staging", "production"]:
                raise ValueError(f"ENVIRONMENT {cls.ENVIRONMENT} must be development, staging, or production")
            
            return True
        except Exception as e:
            print(f"Configuration validation failed: {e}")
            return False

class BackendConfig(Config):
    """Backend-specific configuration extending the base config."""
    
    SERVICE_NAME: str = "backend"
    
    # Uvicorn server configuration
    UVICORN_WORKERS: int = int(os.getenv("UVICORN_WORKERS", "1"))
    RELOAD: bool = os.getenv("RELOAD", "false").lower() == "true"
    
    # Configuration for planned backend middleware:
    # - Authentication: JWT validation, user management
    # - Caching: Redis integration, cache invalidation
    # - Rate limiting: request throttling, client blocking

class FrontendConfig(Config):
    """Frontend-specific configuration."""
    
    SERVICE_NAME: str = "frontend"
    
    # Next.js specific settings
    NEXT_PUBLIC_API_URL: str = os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:8000")
    NODE_ENV: str = os.getenv("NODE_ENV", "development")
    
    # Future frontend-specific middleware settings can be added here:
    # - Authentication configuration
    # - Caching configuration
    # - Rate limiting configuration
    # - Security configuration

# Create configuration instances
backend_config = BackendConfig()
frontend_config = FrontendConfig()

# Validate configurations on import
if not backend_config.validate_config():
    raise ValueError("Backend configuration validation failed")

if not frontend_config.validate_config():
    raise ValueError("Frontend configuration validation failed")
