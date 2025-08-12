"""
Main FastAPI application entry point.
Provides the core API server with health check endpoint, CORS support, logging middleware,
and the core text processing feature.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from middleware import LoggingMiddleware

app = FastAPI(
    title="Interactive Search Engine API",
    description="Backend API for the Interactive Search Engine project",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom logging middleware
app.add_middleware(LoggingMiddleware)


# Request/Response models
class TextProcessRequest(BaseModel):
    """Request model for text processing endpoint."""
    text: str


class TextProcessResponse(BaseModel):
    """Response model for text processing endpoint."""
    result: str


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Status confirmation with message
    """
    return {"status": "healthy", "message": "API is running"}


@app.post("/api/v1/process-text", response_model=TextProcessResponse)
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
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=400, 
            detail="Text field cannot be empty"
        )
    
    # Process the text by adding exclamation points
    processed_text = f"!!! {request.text.strip()} !!!"
    
    return TextProcessResponse(result=processed_text)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
