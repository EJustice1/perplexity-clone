"""
API request and response models for version 1 endpoints.
Defines the data structures used in API communication.
"""

from pydantic import BaseModel, Field, ConfigDict


class SearchRequest(BaseModel):
    """Request model for search endpoint."""

    query: str = Field(
        ..., description="The search query to be processed", examples=["What is artificial intelligence?"]
    )

    model_config = ConfigDict(json_schema_extra={"example": {"query": "What is artificial intelligence?"}})


class SearchResponse(BaseModel):
    """Response model for search endpoint."""

    result: str = Field(
        ...,
        description="The search result response",
        examples=["You searched for: What is artificial intelligence?"],
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"result": "You searched for: What is artificial intelligence?"}}
    )


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(
        ..., description="Health status of the API", examples=["healthy"]
    )

    message: str = Field(..., description="Status message", examples=["API is running"])

    timestamp: str = Field(
        ...,
        description="ISO timestamp of the health check",
        examples=["2025-08-13T21:34:46.123456"],
    )
