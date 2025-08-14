"""
API module initialization.
"""

from fastapi import APIRouter
from api.v1.endpoints import router as v1_router
from api.v1.models import HealthResponse
from datetime import datetime

# Create main API router
api_router = APIRouter()

# Add root-level health endpoint for load balancer
@api_router.get("/health", response_model=HealthResponse)
async def root_health_check():
    """Root-level health check endpoint for load balancer."""
    return HealthResponse(
        status="healthy",
        message="API is running",
        timestamp=datetime.utcnow().isoformat()
    )

# Include v1 endpoints
api_router.include_router(v1_router)
