"""
API endpoints for version 1.
"""

import logging
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from .models import (
    TextProcessRequest,
    TextProcessResponse,
    HealthResponse,
)
from ...services.text_processor import text_processor_service

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


@router.post("/process-text", response_model=TextProcessResponse)
async def process_text(request: TextProcessRequest) -> TextProcessResponse:
    """Process text by adding exclamation points."""
    try:
        logger.info(f"Processing text request: {request.text}")
        
        # Validate input
        if not request.text:
            logger.warning("Empty text received")
            raise ValueError("Text cannot be empty")
            
        processed_text = text_processor_service.process_text(request.text)
        logger.info(f"Text processed successfully: {processed_text}")
        
        return TextProcessResponse(result=processed_text)
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error processing text: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
