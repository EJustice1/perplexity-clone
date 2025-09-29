"""Stage 4 content collation utilities.

This module transforms the Stage 3 multi-search output into cleaned textual
documents by leveraging the existing content extraction service. The results
remain internal until Stage 5 synthesizes answers.
"""

from dataclasses import dataclass, field
import logging
from typing import List, Optional

from src.services.content_extractor import ContentExtractionResult, get_content_extractor
from .multi_search import MultiSearchResponse

logger = logging.getLogger(__name__)


@dataclass
class CollatedDocument:
    """Normalized representation of an extracted document."""

    url: str
    title: str
    text: str
    extraction_method: str


@dataclass
class CollationSummary:
    """Summary statistics for downstream logging and debugging."""

    total_urls: int
    successes: int
    failures: int
    truncated: int
    failure_details: List[str] = field(default_factory=list)


@dataclass
class ContentCollation:
    """Return value produced by the content collator."""

    documents: List[CollatedDocument]
    summary: CollationSummary
    concatenated_text: str


class ContentCollator:
    """Coordinate content extraction over aggregated search results."""

    async def collate(
        self,
        multi_search_response: MultiSearchResponse,
        *,
        max_concurrent: int,
        max_total_chars: int,
    ) -> ContentCollation:
        """Extract and aggregate textual content from multi-search results."""

        extractor = get_content_extractor()
        urls = multi_search_response.aggregated_urls

        if not urls:
            summary = CollationSummary(
                total_urls=0, successes=0, failures=0, truncated=0
            )
            return ContentCollation(documents=[], summary=summary, concatenated_text="")

        extraction_results = await extractor.extract_content_from_urls(
            urls, max_concurrent=max_concurrent
        )

        documents: List[CollatedDocument] = []
        total_chars = 0
        truncated_count = 0
        failure_details: List[str] = []

        for result in extraction_results:
            if not result.success:
                failure_details.append(f"{result.url}: {result.error_message}")
                continue

            text = result.extracted_text or ""
            truncated = False
            if total_chars + len(text) > max_total_chars:
                text = text[: max(0, max_total_chars - total_chars)]
                truncated = True

            if not text:
                continue

            documents.append(
                CollatedDocument(
                    url=result.url,
                    title=result.title,
                    text=text,
                    extraction_method=result.extraction_method,
                )
            )

            total_chars += len(text)
            truncated_count += int(truncated)

            if total_chars >= max_total_chars:
                logger.debug("Reached max_total_chars=%s; stopping aggregation", max_total_chars)
                break

        summary = CollationSummary(
            total_urls=len(urls),
            successes=len(documents),
            failures=len(urls) - len(documents),
            truncated=truncated_count,
            failure_details=failure_details,
        )

        concatenated_text = "\n\n".join(doc.text for doc in documents)
        return ContentCollation(
            documents=documents,
            summary=summary,
            concatenated_text=concatenated_text,
        )

