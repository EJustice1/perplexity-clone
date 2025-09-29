"""Unit tests for the LangChain query decomposition client."""

from typing import Any

import pytest

from src.search import LangChainClient, LangChainConfig


class _FakeChain:
    """Minimal callable stub that records invocations for assertions."""

    def __init__(self, output: str) -> None:
        self.output = output
        self.last_payload: dict[str, Any] | None = None

    def invoke(self, payload: dict[str, Any]) -> str:
        self.last_payload = payload
        return self.output


def test_decompose_query_returns_unique_cleaned_sub_queries() -> None:
    """Client parses line-separated output into a bounded, de-duplicated list."""

    fake_chain = _FakeChain(
        "1. history of mars\n- history of mars missions\n\nMars weather"  # noqa: D400
    )
    config = LangChainConfig(gemini_api_key="stub", max_sub_queries=3)
    client = LangChainClient(config, lambda _: fake_chain)

    result = client.decompose_query(" Mars exploration history ")

    assert result == [
        "history of mars",
        "history of mars missions",
        "Mars weather",
    ]
    assert fake_chain.last_payload == {
        "user_query": "Mars exploration history",
        "max_queries": 3,
    }


def test_decompose_query_falls_back_when_chain_returns_empty() -> None:
    """Empty chain output yields the original trimmed query."""

    fake_chain = _FakeChain("")
    config = LangChainConfig(gemini_api_key="stub")
    client = LangChainClient(config, lambda _: fake_chain)

    result = client.decompose_query("simple question ")

    assert result == ["simple question"]


def test_decompose_query_returns_original_when_not_configured() -> None:
    """Missing API keys keeps behaviour consistent without raising errors."""

    config = LangChainConfig(gemini_api_key=None, google_ai_api_key=None)
    client = LangChainClient(config)

    result = client.decompose_query("What is AI?")

    assert result == ["What is AI?"]


def test_parse_decomposition_output_limits_to_max_queries() -> None:
    """Parser enforces maximum length and strips boilerplate markers."""

    lines = "\n".join(
        [
            "Queries:",
            "* First idea",
            "2. Second idea",
            "Second idea",  # duplicate should be skipped
            "Third idea",
        ]
    )

    parsed = LangChainClient.parse_decomposition_output(lines, max_sub_queries=2)

    assert parsed == ["First idea", "Second idea"]


def test_decompose_query_rejects_empty_input() -> None:
    """Client validates incoming user query strings."""

    config = LangChainConfig(gemini_api_key="stub")
    client = LangChainClient(config, lambda _: _FakeChain("something"))

    with pytest.raises(ValueError):
        client.decompose_query("   ")

