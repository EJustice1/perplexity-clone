# Middleware Architecture Documentation

## Overview

The Perplexity Clone application features a clean, expandable middleware architecture that provides:

- **Metrics Collection** - HTTP request monitoring and performance tracking (fully implemented)
- **Extensible Framework** - Easy to add new middleware types following established patterns

## Architecture Design

### Directory Structure
```
src/
├── middleware/           # Dedicated middleware package
│   ├── __init__.py      # Package initialization and exports
│   ├── base.py          # Base middleware classes and interfaces
│   ├── metrics.py       # Metrics collection middleware (fully implemented)
│   └── README.md        # Package documentation and expansion guide
├── core/                 # Core utilities and configuration
│   ├── config.py        # Centralized configuration
│   └── utils.py         # Common utility functions
├── api/                  # FastAPI backend
└── frontend/            # Flask frontend
```

### Design Principles

1. **Framework Agnostic** - Each middleware has framework-specific implementations
2. **Configurable** - All middleware can be enabled/disabled via configuration
3. **Extensible** - Easy to add new middleware types following established patterns
4. **Composable** - Middleware can be chained together
5. **Testable** - Each middleware is independently testable

## Current Middleware

### 1. Metrics Middleware ✅ (Fully Implemented)

**Purpose**: Collect HTTP request metrics for monitoring and observability.

**Features**:
- Request count tracking (total, by method, endpoint, status, service)
- Request latency histograms
- Prometheus metrics export
- Framework-specific implementations (FastAPI/Flask)

**Usage**:
```python
from src.middleware import create_fastapi_middleware

# Create middleware instance
metrics_middleware = create_fastapi_middleware("backend")

# FastAPI middleware
@app.middleware("http")
async def metrics_handler(request, call_next):
    return await metrics_middleware.metrics_middleware(request, call_next)

# Flask middleware
@app.before_request
def before_request():
    metrics_middleware.before_request(request)

@app.after_request
def after_request(response):
    return metrics_middleware.after_request(request, response)
```

**Configuration**:
```bash
ENABLE_METRICS=true
METRICS_PATH=/metrics
```

## Expanding the Architecture

### Adding New Middleware Types

The architecture is designed to be easily extended. Here's the step-by-step process:

#### Step 1: Create Base Middleware Class

```python
# src/middleware/new_middleware.py
from .base import BaseMiddleware

class NewMiddleware(BaseMiddleware):
    """Base implementation for new middleware type."""
    
    def __init__(self, service_name: str, enabled: bool = True):
        super().__init__(service_name, enabled)
        # Initialize your middleware
    
    def process_request(self, request):
        """Process incoming request."""
        # Your logic here
        return request
    
    def process_response(self, request, response):
        """Process outgoing response."""
        # Your logic here
        return response
```

#### Step 2: Create Framework-Specific Implementations

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

#### Step 3: Add Convenience Functions

```python
def create_fastapi_new_middleware(service_name: str, enabled: bool = True):
    """Create a FastAPI new middleware instance."""
    return FastAPINewMiddleware(service_name, enabled)

def create_flask_new_middleware(service_name: str, enabled: bool = True):
    """Create a Flask new middleware instance."""
    return FlaskNewMiddleware(service_name, enabled)
```

#### Step 4: Update Package Exports

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

#### Step 5: Add Configuration

```python
# src/core/config.py
class Config:
    ENABLE_NEW_MIDDLEWARE: bool = os.getenv("ENABLE_NEW_MIDDLEWARE", "false").lower() == "true"
    
    # New middleware specific settings
    NEW_MIDDLEWARE_SETTING: str = os.getenv("NEW_MIDDLEWARE_SETTING", "default")
```

### Common Middleware Types to Implement

#### Authentication Middleware
- JWT token validation
- Role-based access control
- User session management
- Protected endpoint decorators

#### Caching Middleware
- In-memory caching with TTL
- Redis integration (optional)
- Automatic cache key generation
- Cache statistics and monitoring
- Decorator-based function caching

#### Rate Limiting Middleware
- Configurable rate limits (requests per minute)
- Sliding window algorithm
- Client blocking with configurable duration
- IP-based identification
- Rate limit headers in responses

#### Logging Middleware
- Structured logging
- Correlation IDs
- Request/response logging
- Performance metrics

#### Security Middleware
- CORS handling
- Content Security Policy
- Input validation
- Security headers

#### Compression Middleware
- Gzip compression
- Brotli compression
- Response size optimization
- Configurable compression levels

## Middleware Chaining

### Automatic Chaining

The application can automatically chain all enabled middleware in the correct order:

1. **Rate Limiting** - Check limits first
2. **Authentication** - Validate user identity
3. **Caching** - Check cache for GET requests
4. **Metrics** - Record request start time
5. **Request Processing** - Execute the actual endpoint
6. **Response Processing** - Process response in reverse order

### Manual Chaining

You can also manually chain middleware using the `MiddlewareChain` class:

```python
from src.middleware import MiddlewareChain

# Create a custom chain
chain = MiddlewareChain(
    rate_limit_middleware,
    auth_middleware,
    cache_middleware,
    metrics_middleware
)

# Process request through chain
request = chain.process_request(request)
response = chain.process_response(request, response)
```

## Configuration Management

### Environment Variables

All middleware can be configured via environment variables:

```bash
# Global middleware settings
ENABLE_METRICS=true
ENABLE_NEW_MIDDLEWARE=false  # When you add new middleware

# Service-specific settings
BACKEND_ENABLE_NEW_MIDDLEWARE=true
FRONTEND_ENABLE_NEW_MIDDLEWARE=false

# New middleware specific settings
NEW_MIDDLEWARE_SETTING=value
```

### Configuration Classes

Configuration is managed through Python classes:

```python
from src.core.config import backend_config, frontend_config

# Access configuration
print(f"Service: {backend_config.SERVICE_NAME}")
print(f"New middleware enabled: {backend_config.ENABLE_NEW_MIDDLEWARE}")
```

## Testing Strategy

### Current Status
- **Metrics middleware**: Fully tested and functional

### Testing New Middleware

```python
import pytest
from src.middleware import NewMiddleware

def test_new_middleware():
    middleware = NewMiddleware("test-service")
    
    # Test request processing
    request = MockRequest()
    processed_request = middleware.process_request(request)
    assert processed_request is not None
    
    # Test response processing
    response = MockResponse()
    processed_response = middleware.process_response(request, response)
    assert processed_response is not None
```

## Performance Considerations

### Memory Usage
- **Metrics**: Prometheus handles storage and aggregation
- **Future middleware**: Design with memory efficiency in mind

### Configuration Tuning
```bash
# For high-traffic applications
ENABLE_METRICS=true
ENABLE_NEW_MIDDLEWARE=true

# For development
ENABLE_METRICS=true
ENABLE_NEW_MIDDLEWARE=false
```

## Security Considerations

### Authentication (when implemented)
- JWT tokens with configurable expiry
- Role-based access control
- Secure token storage

### Rate Limiting (when implemented)
- IP-based identification
- Configurable blocking duration
- Automatic cleanup of blocked clients

### Caching (when implemented)
- Excludes sensitive headers from cache keys
- Configurable TTL for different content types
- Cache invalidation strategies

## Best Practices

1. **Follow established patterns** from metrics middleware
2. **Implement both FastAPI and Flask versions**
3. **Use environment variables for configuration**
4. **Add comprehensive logging and error handling**
5. **Make middleware configurable and testable**
6. **Document usage examples and configuration**
7. **Add type hints for better code quality**
8. **Test thoroughly before enabling in production**

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure `src/` is in Python path
2. **Configuration**: Check environment variables are set correctly
3. **Middleware Order**: Check middleware registration order
4. **Framework Compatibility**: Ensure correct implementation for your framework

### Debug Mode
Enable debug logging:
```bash
LOG_LEVEL=DEBUG
```

## Future Enhancements

- **Circuit Breaker** middleware for external service calls
- **Request/Response Transformation** middleware
- **API Versioning** middleware
- **Audit Logging** middleware
- **Distributed Tracing** integration
- **Health Check** middleware for complex services

## Contributing

When adding new middleware:

1. **Study the metrics middleware** implementation
2. **Follow the established patterns** and naming conventions
3. **Create comprehensive tests** before enabling by default
4. **Update configuration** with new environment variables
5. **Document usage examples** in the README
6. **Update implementation status** in `__init__.py`

---

**This architecture provides a solid foundation for scalable, maintainable services with consistent monitoring and easy extensibility.** 🚀
