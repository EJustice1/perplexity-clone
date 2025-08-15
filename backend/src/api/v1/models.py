"""
API request and response models for version 1 endpoints.
Defines the data structures used in API communication.
"""

from pydantic import BaseModel, Field


class TextProcessRequest(BaseModel):
    """Request model for text processing endpoint."""

    text: str = Field(
        ..., description="The text to be processed", example="Hello world"
    )

    class Config:
        json_schema_extra = {"example": {"text": "Hello world"}}


class TextProcessResponse(BaseModel):
    """Response model for text processing endpoint."""

    result: str = Field(
        ...,
        description="The processed text with exclamation points",
        example="!!! Hello world !!!",
    )

    class Config:
        json_schema_extra = {"example": {"result": "!!! Hello world !!!"}}


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(..., description="Health status of the API", example="healthy")

    message: str = Field(..., description="Status message", example="API is running")

    timestamp: str = Field(
        ...,
        description="ISO timestamp of the health check",
        example="2025-08-13T21:34:46.123456",
    )
