# Middleware Package

This package provides a clean, expandable middleware architecture for the Perplexity Clone application.

## Current Implementation Status

| Middleware | Status | Description |
|------------|--------|-------------|
| **Metrics** | ✅ **Fully Implemented** | HTTP request monitoring and Prometheus metrics |

## Architecture Overview

### Base Classes

- **`BaseMiddleware`** - Abstract base class for all middleware
- **`MiddlewareChain`** - Chain multiple middleware together
- **`middleware_decorator`** - Apply middleware to functions

### Framework Support

Each middleware type has framework-specific implementations:
- **FastAPI** - Async middleware with `async def` handlers
- **Flask** - Sync middleware with `before_request`/`after_request`

## Quick Start

### Using Metrics Middleware

```python
from src.middleware import create_fastapi_middleware

# Create and use metrics middleware
metrics_middleware = create_fastapi_middleware("my-service")

@app.middleware("http")
async def metrics_handler(request, call_next):
    return await metrics_middleware.metrics_middleware(request, call_next)
```

## Expanding the Architecture

The middleware architecture is designed to be easily extended. Here's how to add new middleware types:

### 1. Create New Middleware File

```python
# src/middleware/new_middleware.py
from .base import BaseMiddleware

class NewMiddleware(BaseMiddleware):
    """New middleware implementation."""
    
    def __init__(self, service_name: str, enabled: bool = True):
        super().__init__(service_name, enabled)
    
    def process_request(self, request):
        """Process incoming request."""
        # Your logic here
        return request
    
    def process_response(self, request, response):
        """Process outgoing response."""
        # Your logic here
        return response
```

### 2. Create Framework-Specific Implementations

```python
class FastAPINewMiddleware(NewMiddleware):
    """FastAPI-specific implementation."""
    
    async def new_middleware(self, request, call_next):
        """FastAPI middleware handler."""
        request = self.process_request(request)
        response = await call_next(request)
        response = self.process_response(request, response)
        return response

class FlaskNewMiddleware(NewMiddleware):
    """Flask-specific implementation."""
    
    def before_request(self, request):
        """Flask before_request handler."""
        self.process_request(request)
    
    def after_request(self, request, response):
        """Flask after_request handler."""
        return self.process_response(request, response)
```

### 3. Add Convenience Functions

```python
def create_fastapi_new_middleware(service_name: str, enabled: bool = True):
    """Create a FastAPI new middleware instance."""
    return FastAPINewMiddleware(service_name, enabled)

def create_flask_new_middleware(service_name: str, enabled: bool = True):
    """Create a Flask new middleware instance."""
    return FlaskNewMiddleware(service_name, enabled)
```

### 4. Update Package Exports

```python
# src/middleware/__init__.py
from .new_middleware import NewMiddleware, create_fastapi_new_middleware, create_flask_new_middleware

__all__ = [
    # ... existing exports
    "NewMiddleware",
    "create_fastapi_new_middleware",
    "create_flask_new_middleware",
]
```

### 5. Add Configuration

```python
# src/core/config.py
class Config:
    ENABLE_NEW_MIDDLEWARE: bool = os.getenv("ENABLE_NEW_MIDDLEWARE", "false").lower() == "true"
    
    # New middleware specific settings
    NEW_MIDDLEWARE_SETTING: str = os.getenv("NEW_MIDDLEWARE_SETTING", "default")
```

## Common Middleware Types to Add

### Authentication
- JWT token validation
- Role-based access control
- User session management

### Caching
- In-memory caching
- Redis integration
- Cache invalidation strategies

### Rate Limiting
- Request throttling
- Client blocking
- Rate limit headers

### Logging
- Structured logging
- Correlation IDs
- Request/response logging

### Security
- CORS handling
- Content Security Policy
- Input validation

### Compression
- Gzip compression
- Brotli compression
- Response size optimization

## Configuration

Current middleware can be configured via environment variables:

```bash
# Enable/disable metrics middleware
ENABLE_METRICS=true

# Metrics endpoints
METRICS_PATH=/metrics
HEALTH_PATH=/health
```

## Testing

### Current Status
- **Metrics middleware**: Fully tested and functional

### Testing Strategy
```python
def test_metrics_middleware():
    middleware = create_fastapi_middleware("test")
    assert middleware.is_enabled() == True
    assert middleware.service_name == "test"
```

## Dependencies

### Required
- `prometheus-client` - Metrics collection

## Contributing

When adding new middleware:

1. **Follow the established pattern** from metrics middleware
2. **Create framework-specific implementations** (FastAPI/Flask)
3. **Add convenience functions** for easy instantiation
4. **Update package exports** in `__init__.py`
5. **Add configuration options** in `src/core/config.py`
6. **Write comprehensive tests** before enabling by default
7. **Update this README** with usage examples

## Best Practices

1. **Inherit from BaseMiddleware** for consistent interface
2. **Implement both FastAPI and Flask versions** for framework support
3. **Use environment variables** for configuration
4. **Add proper logging** and error handling
5. **Make middleware configurable** (enable/disable, settings)
6. **Follow the naming conventions** established in the codebase
7. **Add type hints** for better code quality

## Support

- **Fully implemented middleware**: Ready for production use
- **Architecture**: Designed for easy expansion
- **Documentation**: See `MIDDLEWARE_ARCHITECTURE.md` for detailed specs
