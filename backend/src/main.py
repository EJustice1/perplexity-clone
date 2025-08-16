"""
Main FastAPI application entry point.
"""

import logging
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .middleware import LoggingMiddleware
from .core.config import settings
from .api import api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Starting {settings.app_name} v{settings.app_version}")
logger.info(f"Environment: {settings.environment}")
logger.info(f"Host: {settings.host}:{settings.port}")

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler to catch any unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    logger.error(f"Request URL: {request.url}")
    logger.error(f"Request method: {request.method}")
    logger.error(f"Request headers: {dict(request.headers)}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc),
            "type": type(exc).__name__,
        },
    )


# Enhanced CORS middleware configuration
logger.info(f"Configuring CORS with origins: {settings.cors_origins}")
logger.info(f"Environment: {settings.environment}")
logger.info(f"Frontend URL: {os.getenv('FRONTEND_URL', 'not set')}")
logger.info(f"Load Balancer URL: {os.getenv('LOAD_BALANCER_URL', 'not set')}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["Content-Length", "Content-Type"],
    max_age=86400,  # Cache preflight response for 24 hours
)

logger.info("Adding LoggingMiddleware")
app.add_middleware(LoggingMiddleware)

logger.info("Including API router")
app.include_router(api_router)

logger.info("Application startup complete")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port)
