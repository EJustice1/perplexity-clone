"""LangChain client implementation for adaptive query decomposition.

Stage 2 introduces dynamic query decomposition by leveraging Gemini through
LangChain. Later stages will expand on this client to add retrieval and answer
synthesis capabilities.
"""

import os
from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

if TYPE_CHECKING:  # pragma: no cover - type checking only
    from .multi_search import MultiQuerySearchOrchestrator, MultiSearchResponse
    from .content_collator import ContentCollator, ContentCollation
    from .answer_synthesizer import AnswerSynthesizer, SynthesizedAnswer

logger = logging.getLogger(__name__)


@dataclass
class LangChainConfig:
    """Configuration values required to initialize LangChain components.

    Attributes:
        serp_api_key: API key used for web search connectors.
        gemini_api_key: API key for Gemini models used via LangChain.
        google_ai_api_key: Legacy Gemini key name supported by existing
            services; used when `gemini_api_key` is not provided.
        model_name: Gemini model used for query decomposition.
        temperature: Sampling temperature for the model.
        max_sub_queries: Upper bound on generated sub-queries.
        per_query_search_results: Number of web search results requested per
            sub-query during multi-search orchestration.
        max_total_search_results: Upper bound on aggregate search results across
            all sub-queries.
        content_extraction_max_concurrent: Maximum concurrent extraction tasks.
        content_extraction_max_total_chars: Upper bound on total characters
            returned in the aggregated context.
        synthesis_model_name: Gemini model used for answer synthesis.
        synthesis_temperature: Temperature for answer synthesis generation.
        synthesis_max_output_tokens: Output token cap for answer synthesis.
    """

    serp_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    google_ai_api_key: Optional[str] = None
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.1
    max_sub_queries: int = 5
    per_query_search_results: int = 2
    max_total_search_results: int = 6
    content_extraction_max_concurrent: int = 3
    content_extraction_max_total_chars: int = 20000
    synthesis_model_name: str = "gemini-2.0-flash"
    synthesis_temperature: float = 0.2
    synthesis_max_output_tokens: int = 768

    @classmethod
    def from_env(cls) -> "LangChainConfig":
        """Create configuration populated from environment variables."""

        return cls(
            serp_api_key=os.getenv("SERPER_API_KEY"),
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            google_ai_api_key=os.getenv("GOOGLE_AI_API_KEY"),
        )

    def get_gemini_api_key(self) -> Optional[str]:
        """Return the available Gemini API key alias, if any."""

        return self.gemini_api_key or self.google_ai_api_key


class LangChainClient:
    """Placeholder client for LangChain-based search orchestration.

    Stage 1 does not instantiate LangChain objects. Future stages will extend
    this class to build query decomposition chains, search retrievers, and RAG
    pipelines using the dependencies installed in this phase.
    """

    def __init__(
        self,
        config: LangChainConfig,
        decomposition_chain_factory: Optional[
            Callable[[LangChainConfig], Any]
        ] = None,
    ) -> None:
        """Store configuration for later initialization.

        Args:
            config: Configuration values required to build LangChain chains.
            decomposition_chain_factory: Optional factory used in tests to
                avoid real API calls.
        """

        self._config = config
        self._decomposition_chain = None
        self._decomposition_chain_factory = decomposition_chain_factory

    def is_configured(self) -> bool:
        """Return True when both mandatory API keys are present."""

        gemini_key = self._config.get_gemini_api_key()
        return bool(gemini_key)

    def decompose_query(self, user_query: str) -> List[str]:
        """Generate up to `max_sub_queries` focused search queries.

        Args:
            user_query: Original query supplied by the user interface.

        Returns:
            Ordered list of one to `max_sub_queries` sub-queries. Falls back to
            the trimmed original query when decomposition is unavailable or no
            valid suggestions are produced.
        """

        cleaned_query = user_query.strip()
        if not cleaned_query:
            raise ValueError("user_query must be a non-empty string")

        if not self.is_configured():
            logger.warning(
                "LangChainClient not configured; returning original query"
            )
            return [cleaned_query]

        try:
            chain = self._ensure_decomposition_chain()
            raw_output = chain.invoke(
                {
                    "user_query": cleaned_query,
                    "max_queries": self._config.max_sub_queries,
                }
            )
            sub_queries = self.parse_decomposition_output(
                raw_output, self._config.max_sub_queries
            )

            if not sub_queries:
                logger.info(
                    "No sub-queries parsed; using original query as fallback"
                )
                return [cleaned_query]

            return sub_queries

        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error(
                "Query decomposition failed; falling back to original query",
                exc_info=exc,
            )
            return [cleaned_query]

    def build_pipeline(self) -> Dict[str, Any]:
        """Return placeholders for pipeline components.

        Future stages will replace this with LangChain chains that perform
        adaptive query decomposition, multi-search retrieval, and answer
        synthesis.
        """

        raise NotImplementedError("LangChain pipeline construction pending")

    async def generate_multi_search_plan(
        self,
        user_query: str,
        orchestrator: "MultiQuerySearchOrchestrator",
    ) -> "MultiSearchResponse":
        """Produce sub-queries and aggregated web search results.

        Args:
            user_query: The original end-user query.
            orchestrator: Executor that runs per-query web searches.

        Returns:
            MultiSearchResponse with sanitized sub-queries and aggregated
            search metadata.
        """

        sub_queries = self.decompose_query(user_query)
        return await orchestrator.run(
            sub_queries=sub_queries,
            per_query_results=self._config.per_query_search_results,
            max_total_results=self._config.max_total_search_results,
        )

    async def collate_content(
        self,
        multi_search_response: "MultiSearchResponse",
        collator: "ContentCollator",
    ) -> "ContentCollation":
        """Aggregate extracted content for the supplied search response."""

        return await collator.collate(
            multi_search_response,
            max_concurrent=self._config.content_extraction_max_concurrent,
            max_total_chars=self._config.content_extraction_max_total_chars,
        )

    async def synthesize_answer(
        self,
        user_query: str,
        collation: "ContentCollation",
        synthesizer: "AnswerSynthesizer",
    ) -> Optional["SynthesizedAnswer"]:
        """Generate an answer grounded in the supplied collation."""

        try:
            return await synthesizer.synthesize(user_query, collation)
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("Answer synthesis failed", exc_info=exc)
            return None

    def _ensure_decomposition_chain(self):
        """Lazily construct the LangChain Runnable used for decomposition."""

        if self._decomposition_chain is not None:
            return self._decomposition_chain

        gemini_key = self._config.get_gemini_api_key()
        if not gemini_key:
            raise RuntimeError("Gemini API key is required for decomposition")

        if self._decomposition_chain_factory:
            self._decomposition_chain = self._decomposition_chain_factory(
                self._config
            )
            return self._decomposition_chain

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You split user questions into at most {max_queries}"
                        " focused web search queries."
                        "\n- Each line must contain a single search query."
                        "\n- Produce fewer queries when the question is simple."
                        "\n- Return the original question unchanged when no"
                        " decomposition helps."
                        "\n- Do not include numbering, bullets, prose, or"
                        " explanations."
                    ),
                ),
                (
                    "human",
                    "User question: {user_query}\nQueries:",
                ),
            ]
        )

        model = ChatGoogleGenerativeAI(
            model=self._config.model_name,
            temperature=self._config.temperature,
            api_key=gemini_key,
        )

        self._decomposition_chain = prompt | model | StrOutputParser()
        return self._decomposition_chain

    @staticmethod
    def parse_decomposition_output(
        raw_output: str, max_sub_queries: int
    ) -> List[str]:
        """Normalize model output into a list of unique queries."""

        if not raw_output:
            return []

        parsed: List[str] = []
        seen = set()

        for line in raw_output.splitlines():
            candidate = line.strip().lstrip("-•*0123456789. ")
            candidate = candidate.strip()
            if not candidate:
                continue
            if candidate.lower() == "queries:" or candidate.lower().startswith(
                "queries"
            ):
                continue
            if candidate not in seen:
                parsed.append(candidate)
                seen.add(candidate)
            if len(parsed) >= max_sub_queries:
                break

        return parsed

