"""
API request and response models for version 1 endpoints.
Defines the data structures used in API communication.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class SearchRequest(BaseModel):
    """Request model for search endpoint."""

    query: str = Field(
        ...,
        description="The search query to be processed",
        examples=["What is artificial intelligence?"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"query": "What is artificial intelligence?"}
        }
    )


class WebSearchResult(BaseModel):
    """Model for individual web search results."""

    title: str = Field(..., description="Title of the search result")
    url: str = Field(..., description="URL of the search result")
    snippet: str = Field(
        ..., description="Snippet/description of the search result"
    )
    source: str = Field(
        default="web_search",
        description="Source of the search result",
    )


class ExtractedContent(BaseModel):
    """Model for extracted content from web pages."""

    url: str = Field(..., description="URL of the source page")
    title: str = Field(..., description="Title of the page")
    extracted_text: str = Field(
        ..., description="Extracted and cleaned text content"
    )
    extraction_method: str = Field(
        ..., description="Method used for content extraction"
    )
    success: bool = Field(
        ..., description="Whether content extraction was successful"
    )
    error_message: Optional[str] = Field(
        None, description="Error message if extraction failed"
    )


class LLMResponse(BaseModel):
    """Model for LLM-generated answer."""

    answer: str = Field(
        ..., description="Synthesized answer from LLM"
    )
    success: bool = Field(
        ..., description="Whether LLM synthesis was successful"
    )
    error_message: Optional[str] = Field(
        None, description="Error message if LLM synthesis failed"
    )
    tokens_used: Optional[int] = Field(
        None, description="Number of tokens used in LLM generation"
    )


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
    extracted_content: List[ExtractedContent] = Field(
        default=[],
        description="List of extracted content from web pages",
    )
    content_summary: Optional[str] = Field(
        None,
        description="Summary of extracted content for verification",
    )
    llm_answer: Optional[LLMResponse] = Field(
        None,
        description="Synthesized answer from LLM based on extracted content",
    )
    citations: Optional[List[str]] = Field(
        default=None,
        description="Ordered list of source URLs referenced in the synthesized answer",
    )
    sub_queries: List[str] = Field(
        default_factory=list,
        description="Ordered list of sub-queries generated during adaptive decomposition",
    )
    original_query: Optional[str] = Field(
        None,
        description="The user's original search query",
    )
    enhanced_query: Optional[str] = Field(
        None,
        description="The enhanced search query used for web search",
    )
    query_enhancement_success: Optional[bool] = Field(
        None,
        description="Whether query enhancement was successful",
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
                ],
                "extracted_content": [
                    {
                        "url": "https://example.com/ai-definition",
                        "title": "What is Artificial Intelligence?",
                        "extracted_text": "Artificial Intelligence (AI) is a branch of computer science...",
                        "extraction_method": "trafilatura",
                        "success": True,
                        "error_message": None,
                    }
                ],
                "content_summary": "Successfully extracted content from 1 out of 1 sources.",
                "llm_answer": {
                    "answer": "Artificial Intelligence (AI) is a branch of computer science that focuses on creating intelligent machines capable of performing tasks that typically require human intelligence.",
                    "success": True,
                    "error_message": None,
                    "tokens_used": 45,
                },
                "citations": [
                    "https://example.com/ai-definition"
                ],
                "sub_queries": [
                    "artificial intelligence definition"
                ],
            }
        }
    )


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(
        ...,
        description="Health status of the API",
        examples=["healthy"],
    )

    message: str = Field(
        ...,
        description="Status message",
        examples=["API is running"],
    )

    timestamp: str = Field(
        ...,
        description="ISO timestamp of the health check",
        examples=["2025-08-13T21:34:46.123456"],
    )


class TopicSubscriptionRequest(BaseModel):
    """Request payload for creating a topic subscription."""

    email: str = Field(
        ...,
        description="Subscriber email address",
        examples=["user@example.com"],
    )
    topic: str = Field(
        ...,
        description="Topic the subscriber wants weekly updates for",
        examples=["Generative AI"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "topic": "Generative AI",
            }
        }
    )


class TopicSubscriptionResponse(BaseModel):
    """Response payload returned after creating a subscription."""

    subscription_id: str = Field(
        ...,
        description="Unique identifier assigned to the subscription",
        examples=["a1b2c3d4"],
    )
    message: str = Field(
        ...,
        description="Human-friendly confirmation message",
        examples=["Subscription created"],
    )
