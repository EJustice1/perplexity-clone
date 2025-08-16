"""
API endpoints for version 1.
"""

import logging
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from .models import (
    SearchRequest,
    SearchResponse,
    HealthResponse,
)
from ...services.text_processor import search_service

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="API is running",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """Process search query and return a simple response."""
    try:
        logger.info(f"Processing search request: {request.query}")
        
        # Validate input
        if not request.query:
            logger.warning("Empty search query received")
            raise ValueError("Search query cannot be empty")
            
        search_result = search_service.search(request.query)
        logger.info(f"Search processed successfully: {search_result}")
        
        return SearchResponse(result=search_result)
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error processing search: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
