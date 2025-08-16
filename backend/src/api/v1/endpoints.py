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
    WebSearchResult,
)
from ...services.web_search import get_web_search_service

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
    """Process search query and return web search results."""
    try:
        logger.info(f"Processing search request: {request.query}")

        # Validate input
        if not request.query or not request.query.strip():
            logger.warning("Empty or whitespace-only search query received")
            raise ValueError("Search query cannot be empty")

        # Get web search service and perform search
        web_search_service = get_web_search_service()
        search_results = await web_search_service.search(request.query, max_results=5)

        # Convert to API response format
        sources = [
            WebSearchResult(
                title=result.title,
                url=result.url,
                snippet=result.snippet,
                source=result.source,
            )
            for result in search_results
        ]

        logger.info(f"Web search completed successfully, found {len(sources)} results")

        return SearchResponse(sources=sources)

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error processing search: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
