"""Stage 5 answer synthesis utilities.

This module converts collated content into grounded answers using Gemini via
LangChain. The output remains internal until the API is updated in Stage 6.
"""

from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING, Dict, List, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

if TYPE_CHECKING:  # pragma: no cover - typing only
    from .content_collator import CollatedDocument, ContentCollation

logger = logging.getLogger(__name__)


@dataclass
class SynthesizedAnswer:
    """Return value from the Stage 5 synthesizer."""

    answer: str
    cited_urls: List[str]
    prompt_tokens_used: Optional[int] = None
    completion_tokens_used: Optional[int] = None


class AnswerSynthesizer:
    """Generate grounded answers from collated documents."""

    def __init__(
        self,
        *,
        model_name: str,
        temperature: float,
        max_output_tokens: int,
        api_key: Optional[str],
        chain_override: Optional[object] = None,
    ) -> None:
        if not api_key:
            self._model = None
        else:
            self._model = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                api_key=api_key,
                max_output_tokens=max_output_tokens,
            )
        if self._model is not None:
            self._parser = StrOutputParser()
            self._prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        (
                            "You are a research assistant. Answer the user's question "
                            "using ONLY the provided documents. Cite sources using "
                            "inline markers like [1]. If the documents do not contain "
                            "sufficient information, respond with 'I could not find "
                            "information about that in the retrieved context.'"
                        ),
                    ),
                    (
                        "human",
                        "Question: {question}\n\nDocuments:\n{document_block}",
                    ),
                ]
            )
        else:
            self._parser = None
            self._prompt = None
        self._chain_override = chain_override

    async def synthesize(
        self,
        question: str,
        collation: "ContentCollation",
    ) -> SynthesizedAnswer:
        """Return a grounded answer based on the supplied documents."""

        if not collation.documents:
            logger.info("No documents available; returning insufficient context message")
            return SynthesizedAnswer(
                answer="I could not find information about that in the retrieved context.",
                cited_urls=[],
            )

        if self._model is None or self._parser is None or self._prompt is None:
            logger.info("Answer synthesis skipped; Gemini model not configured")
            return SynthesizedAnswer(
                answer="I could not find information about that in the retrieved context.",
                cited_urls=[doc.url for doc in collation.documents],
            )

        document_block = self._build_document_block(collation.documents)
        chain = self._chain_override or (self._prompt | self._model | self._parser)

        raw_answer = await chain.ainvoke({"question": question, "document_block": document_block})
        cited_urls = [doc.url for doc in collation.documents]

        return SynthesizedAnswer(answer=raw_answer.strip(), cited_urls=cited_urls)

    @staticmethod
    def _build_document_block(documents: List["CollatedDocument"]) -> str:
        """Return prompt-friendly block with numbered sources."""

        parts = []
        for idx, doc in enumerate(documents, 1):
            parts.append(
                f"[{idx}] Title: {doc.title or 'Untitled'}\nURL: {doc.url}\nContent: {doc.text}"
            )
        return "\n\n".join(parts)

