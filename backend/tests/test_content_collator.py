"""Stage 4 content collation tests."""

from typing import List

import pytest

from src.search import ContentCollator, MultiSearchResponse
from src.search.content_collator import CollatedDocument


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


class _FakeExtractionResult:
    def __init__(self, success: bool, url: str, text: str, method: str, title: str = "Title"):
        self.success = success
        self.url = url
        self.extracted_text = text
        self.extraction_method = method
        self.title = title
        self.error_message = "boom" if not success else None


pytestmark = pytest.mark.anyio


async def test_collator_filters_failures_and_truncates(monkeypatch: pytest.MonkeyPatch) -> None:
    response = MultiSearchResponse(sub_queries=["a"], per_query_outcomes=[], aggregated_urls=["u1", "u2"])
    fake_results = [
        _FakeExtractionResult(True, "u1", "x" * 10, "trafilatura"),
        _FakeExtractionResult(False, "u2", "", "failed"),
    ]

    class _FakeExtractor:
        async def extract_content_from_urls(self, urls: List[str], max_concurrent: int):
            return fake_results

    monkeypatch.setattr("src.search.content_collator.get_content_extractor", lambda: _FakeExtractor())

    collator = ContentCollator()
    result = await collator.collate(response, max_concurrent=2, max_total_chars=5)

    assert result.summary.successes == 1
    assert result.summary.failures == 1
    assert result.documents[0].url == "u1"
    assert len(result.documents[0].text) == 5


async def test_collator_returns_empty_when_no_urls(monkeypatch: pytest.MonkeyPatch) -> None:
    response = MultiSearchResponse(sub_queries=[], per_query_outcomes=[], aggregated_urls=[])

    collator = ContentCollator()
    result = await collator.collate(response, max_concurrent=1, max_total_chars=100)

    assert result.documents == []
    assert result.summary.total_urls == 0
    assert result.concatenated_text == ""


async def test_collator_concatenates_multiple_documents(monkeypatch: pytest.MonkeyPatch) -> None:
    response = MultiSearchResponse(sub_queries=["sq"], per_query_outcomes=[], aggregated_urls=["a", "b"])
    fake_results = [
        _FakeExtractionResult(True, "a", "Doc1", "trafilatura"),
        _FakeExtractionResult(True, "b", "Doc2", "trafilatura"),
    ]

    class _FakeExtractor:
        async def extract_content_from_urls(self, urls: List[str], max_concurrent: int):
            return fake_results

    monkeypatch.setattr("src.search.content_collator.get_content_extractor", lambda: _FakeExtractor())

    collator = ContentCollator()
    result = await collator.collate(response, max_concurrent=2, max_total_chars=20)

    assert result.summary.successes == 2
    assert result.concatenated_text == "Doc1\n\nDoc2"

    for doc in result.documents:
        assert isinstance(doc, CollatedDocument)

