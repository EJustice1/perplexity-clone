"""
API endpoints for version 1.
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from api.v1.models import TextProcessRequest, TextProcessResponse, HealthResponse
from services.text_processor import text_processor_service

router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="API is running",
        timestamp=datetime.utcnow().isoformat()
    )


@router.post("/process-text", response_model=TextProcessResponse)
async def process_text(request: TextProcessRequest):
    """Process text by adding exclamation points."""
    try:
        processed_text = text_processor_service.process_text(request.text)
        return TextProcessResponse(result=processed_text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
