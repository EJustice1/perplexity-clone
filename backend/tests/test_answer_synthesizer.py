"""Tests for Stage 5 answer synthesizer."""

from typing import List

import pytest

from src.search import AnswerSynthesizer, CollatedDocument, ContentCollation, CollationSummary


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


class _FakeModel:
    def __init__(self, response: str) -> None:
        self.response = response
        self.calls: List[dict] = []

    async def ainvoke(self, payload: dict) -> str:
        self.calls.append(payload)
        return self.response


class _FakeSynthesizer(AnswerSynthesizer):
    def __init__(self, response: str) -> None:
        # bypass parent init to avoid real model
        self._model = _FakeModel(response)
        self._parser = lambda x: x
        self._prompt = lambda **kwargs: kwargs

    async def synthesize(self, question: str, collation: ContentCollation):
        return await super().synthesize(question, collation)  # type: ignore


def _build_collation(texts: List[str]) -> ContentCollation:
    documents = [
        CollatedDocument(url=f"https://example.com/{idx}", title=f"Doc {idx}", text=text, extraction_method="trafilatura")
        for idx, text in enumerate(texts, 1)
    ]
    summary = CollationSummary(total_urls=len(texts), successes=len(texts), failures=0, truncated=0)
    return ContentCollation(documents=documents, summary=summary, concatenated_text="\n\n".join(texts))


@pytest.mark.anyio
async def test_synthesizer_handles_empty_collation(monkeypatch: pytest.MonkeyPatch) -> None:
    synthesizer = AnswerSynthesizer(
        model_name="test",
        temperature=0.1,
        max_output_tokens=128,
        api_key="dummy",
    )

    result = await synthesizer.synthesize("What is AI?", _build_collation([]))

    assert "could not find" in result.answer
    assert result.cited_urls == []


@pytest.mark.anyio
async def test_synthesizer_invokes_model_with_documents(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_model = _FakeModel("Answer")

    synthesizer = AnswerSynthesizer(
        model_name="test",
        temperature=0.1,
        max_output_tokens=128,
        api_key="dummy",
        chain_override=fake_model,
    )

    collation = _build_collation(["Doc text"])
    result = await synthesizer.synthesize("Question", collation)

    assert result.answer == "Answer"
    assert result.cited_urls == ["https://example.com/1"]
    assert fake_model.calls
    payload = fake_model.calls[0]
    assert "Question" in payload["question"]
    assert "Doc text" in payload["document_block"]

