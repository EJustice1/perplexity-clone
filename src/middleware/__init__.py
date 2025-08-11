"""
Middleware package for the Perplexity Clone application.
This package provides expandable middleware architecture for metrics and future middleware types.

The architecture is designed to be easily extended with new middleware types
by following the established patterns and base classes.
"""

from .base import BaseMiddleware, MiddlewareChain, middleware_decorator
from .metrics import MetricsMiddleware, create_fastapi_middleware, create_flask_middleware

# Convenience imports for common use cases
__all__ = [
    # Base classes and utilities
    "BaseMiddleware",
    "MiddlewareChain", 
    "middleware_decorator",
    
    # Fully implemented middleware
    "MetricsMiddleware",
    "create_fastapi_middleware",
    "create_flask_middleware",
]

# Version information
__version__ = "1.0.0"
__author__ = "Perplexity Clone Team"

# Implementation status
IMPLEMENTATION_STATUS = {
    "metrics": "fully_implemented"
}

# Future middleware types that can be added:
# - Authentication (JWT, RBAC)
# - Caching (Redis, in-memory)
# - Rate Limiting (throttling, blocking)
# - Logging (structured logging, correlation IDs)
# - Validation (request/response validation)
# - Compression (gzip, brotli)
# - Security (CORS, CSP, rate limiting)
