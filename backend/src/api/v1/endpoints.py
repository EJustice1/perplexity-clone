"""
API endpoints for version 1 of the API.
Contains route handlers and request/response logic.
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from .models import TextProcessRequest, TextProcessResponse, HealthResponse
from ...services.text_processor import text_processor_service

# Create router for v1 endpoints
router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        HealthResponse: Status confirmation with message and timestamp
    """
    return HealthResponse(
        status="healthy",
        message="API is running",
        timestamp=datetime.utcnow().isoformat()
    )


@router.post("/process-text", response_model=TextProcessResponse)
async def process_text(request: TextProcessRequest):
    """
    Core text processing endpoint that adds exclamation points around the input text.
    
    Args:
        request: TextProcessRequest containing the text to process
        
    Returns:
        TextProcessResponse: The processed text with exclamation points
        
    Raises:
        HTTPException: If the text field is empty or invalid
    """
    try:
        # Use service layer for business logic
        processed_text = text_processor_service.process_text(request.text)
        
        return TextProcessResponse(result=processed_text)
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        # Log unexpected errors (you can add logging here later)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
