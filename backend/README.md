# Perplexity Clone Backend

AI-powered search API backend built with FastAPI and modern Python practices.

## Features

- **FastAPI Framework**: High-performance async web framework
- **Middleware Architecture**: Extensible middleware system for metrics, auth, caching
- **Prometheus Metrics**: Built-in monitoring and observability
- **Docker Support**: Containerized deployment
- **Type Safety**: Full type hints and validation

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -e .

# Run development server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Using Docker

```bash
# Build and run
docker build -t perplexity-backend .
docker run -p 8000:8000 perplexity-backend
```

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `GET /metrics` - Prometheus metrics
- `GET /docs` - Interactive API documentation

## Middleware

The backend includes a modular middleware system:

- **Metrics Middleware**: Request monitoring and Prometheus integration
- **Base Classes**: Extensible foundation for new middleware types
- **Framework Support**: FastAPI and Flask implementations

## Configuration

Environment variables:

```bash
SERVICE_NAME=backend
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
ENABLE_METRICS=true
```

## Development

### Code Quality

```bash
# Format code
black src/
isort src/

# Lint code
flake8 src/
mypy src/

# Run tests
pytest
```

### Adding New Middleware

1. Create new middleware class inheriting from `BaseMiddleware`
2. Implement `process_request` and `process_response` methods
3. Add framework-specific implementations if needed
4. Update package exports in `src/middleware/__init__.py`

## Deployment

### Docker

```bash
docker build -t perplexity-backend .
docker run -p 8000:8000 perplexity-backend
```

### Environment Variables

Set required environment variables for production:

```bash
ENVIRONMENT=production
ENABLE_METRICS=true
LOG_LEVEL=INFO
```

## Monitoring

- **Health Checks**: `/health` endpoint for service monitoring
- **Metrics**: Prometheus metrics at `/metrics`
- **Logging**: Structured logging with configurable levels

## Contributing

1. Follow the established middleware patterns
2. Add type hints to all functions
3. Include docstrings for public methods
4. Run tests and linting before submitting
