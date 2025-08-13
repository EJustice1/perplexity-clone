"""
API router configuration.
Organizes and includes all API versions and endpoints.
"""

from fastapi import APIRouter
from .v1.endpoints import router as v1_router

# Main API router
api_router = APIRouter()

# Include v1 endpoints
api_router.include_router(v1_router)
