"""
API module initialization.
"""

from fastapi import APIRouter
from api.v1.endpoints import router as v1_router

# Create main API router
api_router = APIRouter()

# Include v1 endpoints
api_router.include_router(v1_router)
