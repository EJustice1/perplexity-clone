from fastapi import FastAPI, Request, Response
from src.middleware import (
    create_fastapi_middleware,
    get_metrics_response,
    get_health_response
)
from src.core.config import backend_config

app = FastAPI()

# Create metrics middleware instance (fully functional)
metrics_middleware = create_fastapi_middleware(backend_config.SERVICE_NAME)

# Note: Auth, caching, and rate limiting middleware are skeletons and disabled by default
# They can be enabled and implemented later when needed

@app.middleware("http")
async def metrics_middleware_handler(request: Request, call_next):
    """Metrics middleware for FastAPI."""
    return await metrics_middleware.metrics_middleware(request, call_next)

@app.get("/")
async def root():
    return {"message": "Backend is running"}

@app.get("/metrics")
async def metrics():
    """Standardized metrics endpoint."""
    content, media_type = get_metrics_response()
    return Response(content=content, media_type=media_type)

@app.get("/health")
async def health():
    """Standardized health endpoint."""
    return get_health_response(backend_config.SERVICE_NAME)

# TODO: Add these endpoints when middleware is fully implemented
# @app.get("/protected")
# async def protected_endpoint():
#     """Protected endpoint requiring authentication."""
#     return {"message": "This is a protected endpoint", "user": "authenticated"}

# @app.get("/cache-test")
# async def cache_test():
#     """Test endpoint for caching."""
#     import time
#     return {"message": "Cached response", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=backend_config.API_HOST, 
        port=backend_config.API_PORT,
        reload=backend_config.RELOAD,
        workers=backend_config.UVICWORKERS
    )
