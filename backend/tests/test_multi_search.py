"""Tests for Stage 3 multi-sub-query web search orchestration."""

from typing import List

import pytest

from src.search import (
    LangChainConfig,
    LangChainClient,
    MultiQuerySearchOrchestrator,
    MultiSearchResponse,
)
from src.services.web_search import WebSearchResult

pytestmark = pytest.mark.anyio


class _FakeWebSearchService:
    """Minimal fake service that returns prepared responses per query."""

    def __init__(self, mapping: dict[str, List[str]]) -> None:
        self.mapping = mapping
        self.calls: list[tuple[str, int]] = []

    async def search(self, query: str, max_results: int = 5):
        self.calls.append((query, max_results))
        urls = self.mapping.get(query, [])[:max_results]
        return [
            WebSearchResult(title=f"Title for {url}", url=url, snippet="snip")
            for url in urls
        ]


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_orchestrator_runs_searches_and_deduplicates_urls(anyio_backend: str) -> None:
    mapping = {
        "query a": ["https://example.com/a1", "https://example.com/a2"],
        "query b": ["https://example.com/a2", "https://example.com/b1"],
    }
    fake_service = _FakeWebSearchService(mapping)
    orchestrator = MultiQuerySearchOrchestrator(web_search_service=fake_service)

    result = await orchestrator.run(
        sub_queries=["query a", "query b"],
        per_query_results=2,
        max_total_results=3,
    )

    assert result.sub_queries == ["query a", "query b"]
    assert fake_service.calls == [("query a", 2), ("query b", 2)]
    assert result.aggregated_urls == [
        "https://example.com/a1",
        "https://example.com/a2",
        "https://example.com/b1",
    ]
    assert all(outcome.error is None for outcome in result.per_query_outcomes)


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_orchestrator_handles_empty_input_gracefully(anyio_backend: str) -> None:
    orchestrator = MultiQuerySearchOrchestrator(web_search_service=_FakeWebSearchService({}))

    result = await orchestrator.run(
        sub_queries=["  "],
        per_query_results=2,
        max_total_results=3,
    )

    assert result.sub_queries == []
    assert result.aggregated_urls == []
    assert result.per_query_outcomes == []


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_orchestrator_records_errors_without_stopping(anyio_backend: str) -> None:
    class _ErroringService(_FakeWebSearchService):
        async def search(self, query: str, max_results: int = 5):
            raise RuntimeError("boom")

    service = _ErroringService({})
    orchestrator = MultiQuerySearchOrchestrator(web_search_service=service)

    result = await orchestrator.run(
        sub_queries=["issue"],
        per_query_results=1,
        max_total_results=2,
    )

    assert result.sub_queries == ["issue"]
    assert result.aggregated_urls == []
    assert len(result.per_query_outcomes) == 1
    assert result.per_query_outcomes[0].error == "boom"


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_langchain_client_generate_multi_search_plan_integration(anyio_backend: str) -> None:
    config = LangChainConfig(gemini_api_key="stub", max_sub_queries=2)
    client = LangChainClient(
        config,
        decomposition_chain_factory=lambda _: _FakeChain("Query A\nQuery B"),
    )

    mapping = {
        "Query A": ["https://example.com/a"],
        "Query B": ["https://example.com/b"],
    }
    orchestrator = MultiQuerySearchOrchestrator(
        web_search_service=_FakeWebSearchService(mapping)
    )

    response = await client.generate_multi_search_plan("Original Question", orchestrator)

    assert isinstance(response, MultiSearchResponse)
    assert response.sub_queries == ["Query A", "Query B"]
    assert response.aggregated_urls == [
        "https://example.com/a",
        "https://example.com/b",
    ]


class _FakeChain:
    def __init__(self, output: str) -> None:
        self.output = output

    def invoke(self, payload):
        return self.output
