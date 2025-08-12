"""
Main FastAPI application entry point.
Provides the core API server with health check endpoint.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Interactive Search Engine API",
    description="Backend API for the Interactive Search Engine project",
    version="0.1.0"
)


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Status confirmation with message
    """
    return {"status": "healthy", "message": "API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
