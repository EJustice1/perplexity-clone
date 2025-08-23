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
    ExtractedContent,
)
from ...services.web_search import get_web_search_service
from ...services.content_extractor import get_content_extractor
from ...services.llm_synthesis import get_llm_synthesis_service

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
    """Process search query and return web search results with extracted content."""
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

        # Extract content from the top 3-5 results
        extracted_content = []
        content_summary = ""
        
        if sources:
            # Get URLs from search results
            urls = [source.url for source in sources[:3]]  # Limit to top 3 for performance
            
            # Extract content from URLs
            content_extractor = get_content_extractor()
            extraction_results = await content_extractor.extract_content_from_urls(urls, max_concurrent=2)
            
            # Convert to API response format
            extracted_content = [
                ExtractedContent(
                    url=result.url,
                    title=result.title,
                    extracted_text=result.extracted_text,
                    extraction_method=result.extraction_method,
                    success=result.success,
                    error_message=result.error_message,
                )
                for result in extraction_results
            ]
            
            # Generate content summary
            successful_extractions = sum(1 for content in extracted_content if content.success)
            total_attempts = len(extracted_content)
            
            if successful_extractions > 0:
                content_summary = f"Successfully extracted content from {successful_extractions} out of {total_attempts} sources."
                if successful_extractions < total_attempts:
                    content_summary += f" {total_attempts - successful_extractions} extractions failed."
            else:
                content_summary = "Content extraction failed for all sources."
            
            logger.info(f"Content extraction completed: {successful_extractions}/{total_attempts} successful")

        # Step 4: LLM Synthesis (Stage 4 implementation)
        llm_answer = None
        if extracted_content and any(content.success for content in extracted_content):
            try:
                logger.info("Starting LLM synthesis process")
                llm_service = get_llm_synthesis_service()
                
                if llm_service.is_configured():
                    llm_response = await llm_service.synthesize_answer(
                        request.query, 
                        extracted_content
                    )
                    
                    if llm_response.success:
                        logger.info("LLM synthesis completed successfully")
                        # Convert interface response to API model format
                        llm_answer = LLMResponse(
                            answer=llm_response.content,
                            success=llm_response.success,
                            error_message=llm_response.error_message,
                            tokens_used=llm_response.tokens_used
                        )
                    else:
                        logger.warning(f"LLM synthesis failed: {llm_response.error_message}")
                        # Continue without LLM answer - user still gets sources and extracted content
                else:
                    logger.info("LLM service not configured, skipping synthesis")
                    
            except Exception as e:
                logger.error(f"Error in LLM synthesis: {str(e)}", exc_info=True)
                # Continue without LLM answer - user still gets sources and extracted content

        return SearchResponse(
            sources=sources,
            extracted_content=extracted_content,
            content_summary=content_summary,
            llm_answer=llm_answer,
        )

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error processing search: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
