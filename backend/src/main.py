"""
Main FastAPI application entry point.
Provides the core API server with proper architecture, CORS support, 
logging middleware, and organized API routing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware import LoggingMiddleware
from core.config import settings
from api import api_router

# Create FastAPI application with configuration from settings
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version
)

# Add CORS middleware with configuration from settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add custom logging middleware
app.add_middleware(LoggingMiddleware)

# Include API routes
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.host, 
        port=settings.port
    )
