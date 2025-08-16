"""
API request and response models for version 1 endpoints.
Defines the data structures used in API communication.
"""

from typing import List
from pydantic import BaseModel, Field, ConfigDict


class SearchRequest(BaseModel):
    """Request model for search endpoint."""

    query: str = Field(
        ...,
        description="The search query to be processed",
        examples=["What is artificial intelligence?"],
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"query": "What is artificial intelligence?"}}
    )


class WebSearchResult(BaseModel):
    """Model for individual web search results."""

    title: str = Field(..., description="Title of the search result")
    url: str = Field(..., description="URL of the search result")
    snippet: str = Field(..., description="Snippet/description of the search result")
    source: str = Field(default="web_search", description="Source of the search result")


class SearchResponse(BaseModel):
    """Response model for search endpoint."""

    sources: List[WebSearchResult] = Field(
        ...,
        description="List of web search results",
        examples=[
            [
                {
                    "title": "What is Artificial Intelligence?",
                    "url": "https://example.com/ai-definition",
                    "snippet": "Artificial Intelligence (AI) is a branch of computer science...",
                    "source": "web_search",
                }
            ]
        ],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "sources": [
                    {
                        "title": "What is Artificial Intelligence?",
                        "url": "https://example.com/ai-definition",
                        "snippet": "Artificial Intelligence (AI) is a branch of computer science...",
                        "source": "web_search",
                    }
                ]
            }
        }
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
