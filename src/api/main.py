from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from src.middleware import (
    create_fastapi_middleware,
    get_metrics_response,
    get_health_response
)
from src.core.config import backend_config

app = FastAPI(
    title="Perplexity Clone API",
    description="AI-powered search API backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=backend_config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize metrics middleware for request monitoring
metrics_middleware = create_fastapi_middleware(backend_config.SERVICE_NAME)

@app.middleware("http")
async def metrics_middleware_handler(request: Request, call_next):
    """HTTP middleware handler for collecting request metrics."""
    return await metrics_middleware.metrics_middleware(request, call_next)

@app.get("/")
async def root():
    return {"message": "Backend is running"}

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint for monitoring."""
    content, media_type = get_metrics_response()
    return Response(content=content, media_type=media_type)

@app.get("/health")
async def health():
    """Health check endpoint for service monitoring."""
    return get_health_response(backend_config.SERVICE_NAME)

# Future endpoint implementations for planned middleware:
# - /protected - Authentication middleware
# - /cache-test - Caching middleware
# - /rate-limit-test - Rate limiting middleware

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=backend_config.API_HOST, 
        port=backend_config.API_PORT,
        reload=backend_config.RELOAD,
        workers=backend_config.UVICORN_WORKERS
    )
