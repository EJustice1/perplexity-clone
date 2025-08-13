"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware import LoggingMiddleware
from core.config import settings
from api import api_router

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port
    )
