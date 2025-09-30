"""
API endpoints for version 1.
"""

import logging
import re
import asyncio
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, HTTPException, status

from .models import (
    SearchRequest,
    SearchResponse,
    HealthResponse,
    WebSearchResult,
    ExtractedContent,
    LLMResponse,
    TopicSubscriptionRequest,
    TopicSubscriptionResponse,
)
from ...search import (
    LangChainClient,
    LangChainConfig,
    MultiQuerySearchOrchestrator,
    ContentCollator,
    AnswerSynthesizer,
)
from ...services.firestore_subscription_service import (
    FirestoreSubscriptionService,
    FirestoreClientError,
)
from ...core.app_settings import app_settings

# Single Firestore service instance (lazy-loaded)
firestore_service: FirestoreSubscriptionService | None = None

EMAIL_PATTERN = re.compile(
    r"^(?:[a-zA-Z0-9_'^&/+-])+(?:\.(?:[a-zA-Z0-9_'^&/+-])+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
)

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["v1"])


def _get_firestore_service() -> FirestoreSubscriptionService:
    """Return a singleton FirestoreSubscriptionService instance."""

    global firestore_service  # noqa: PLW0603 - module-level singleton

    if firestore_service is not None:
        return firestore_service

    if not app_settings.gcp_project_id:
        raise RuntimeError("GCP_PROJECT_ID environment variable is not configured")

    collection = app_settings.firestore_collection or "topic_subscriptions"

    firestore_service = FirestoreSubscriptionService(
        project_id=app_settings.gcp_project_id,
        collection_name=collection,
    )

    return firestore_service


async def _persist_subscription(
    email: str, topic: str
) -> TopicSubscriptionResponse:
    """Persist the subscription to Firestore and return response payload."""

    service = _get_firestore_service()
    record = await asyncio.to_thread(service.create_subscription, email, topic)

    return TopicSubscriptionResponse(
        subscription_id=record.subscription_id,
        message="Subscription created.",
    )


@router.post(
    "/subscriptions",
    response_model=TopicSubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription(
    request: TopicSubscriptionRequest,
) -> TopicSubscriptionResponse:
    """Create a new topic subscription and persist it to Firestore."""

    email = request.email.strip().lower()
    topic = request.topic.strip()

    if not email or not EMAIL_PATTERN.match(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email address provided.",
        )

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Topic cannot be empty.",
        )

    try:
        return await _persist_subscription(email=email, topic=topic)
    except FirestoreClientError as exc:
        logger.error("Failed to persist subscription", exc_info=exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to store subscription. Please try again later.",
        ) from exc



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
            logger.warning(
                "Empty or whitespace-only search query received"
            )
            raise ValueError("Search query cannot be empty")

        config = LangChainConfig.from_env()
        client = LangChainClient(config)

        # Stage 2: adaptive query decomposition
        sub_queries = client.decompose_query(request.query)

        # Stage 3: multi-subquery web search
        orchestrator = MultiQuerySearchOrchestrator()
        multi_search = await client.generate_multi_search_plan(
            request.query, orchestrator
        )

        sources: List[WebSearchResult] = []
        seen_urls = set()
        for outcome in multi_search.per_query_outcomes:
            for result in outcome.results:
                if not result.url or result.url in seen_urls:
                    continue
                seen_urls.add(result.url)
                sources.append(
                    WebSearchResult(
                        title=result.title,
                        url=result.url,
                        snippet=result.snippet,
                        source="web_search",
                    )
                )

        for url in multi_search.aggregated_urls:
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            sources.append(
                WebSearchResult(
                    title="",
                    url=url,
                    snippet="",
                    source="web_search",
                )
            )

        # Stage 4: content collation
        collator = ContentCollator()
        collation = await client.collate_content(multi_search, collator)

        extracted_content = []
        for doc in collation.documents:
            extracted_content.append(
                ExtractedContent(
                    url=doc.url,
                    title=doc.title,
                    extracted_text=doc.text,
                    extraction_method=doc.extraction_method,
                    success=True,
                    error_message=None,
                )
            )

        for detail in collation.summary.failure_details:
            split_detail = detail.split(": ", maxsplit=1)
            failure_url = split_detail[0]
            message = split_detail[1] if len(split_detail) > 1 else detail
            extracted_content.append(
                ExtractedContent(
                    url=failure_url,
                    title="",
                    extracted_text="",
                    extraction_method="failed",
                    success=False,
                    error_message=message,
                )
            )

        if not extracted_content:
            extracted_content = []

        content_summary = "No sources available for extraction."
        if collation.summary.successes:
            content_summary = (
                f"Successfully extracted content from {collation.summary.successes} out of {collation.summary.total_urls} sources."
            )
            if collation.summary.failures:
                content_summary += (
                    f" {collation.summary.failures} extractions failed."
                )
        elif collation.summary.total_urls:
            content_summary = "Content extraction failed for all sources."

        # Stage 5: answer synthesis
        citations = None
        llm_answer = None
        try:
            synthesizer = AnswerSynthesizer(
                model_name=config.synthesis_model_name,
                temperature=config.synthesis_temperature,
                max_output_tokens=config.synthesis_max_output_tokens,
                api_key=config.get_gemini_api_key(),
            )
            synthesized_answer = await client.synthesize_answer(
                request.query, collation, synthesizer
            )

            if synthesized_answer is not None:
                llm_answer = LLMResponse(
                    answer=synthesized_answer.answer,
                    success=True,
                    error_message=None,
                    tokens_used=None,
                )
                citations = synthesized_answer.cited_urls
        except ValueError:
            logger.info("Gemini API key missing; skipping answer synthesis")
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("Answer synthesis failed", exc_info=exc)

        original_query = request.query
        enhanced_query = request.query
        enhancement_success = None

        return SearchResponse(
            sources=sources,
            extracted_content=extracted_content,
            content_summary=content_summary,
            llm_answer=llm_answer,
            citations=citations,
            sub_queries=list(sub_queries),
            original_query=original_query,
            enhanced_query=enhanced_query,
            query_enhancement_success=enhancement_success,
        )

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(
            f"Unexpected error processing search: {str(e)}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=500, detail="Internal server error"
        )
