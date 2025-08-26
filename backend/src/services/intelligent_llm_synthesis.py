"""
Intelligent LLM Synthesis Service for generating adaptive, question-aware answers.

This service implements a three-stage intelligent prompting system:
1. Question Analysis: Determines optimal response format and detail level
2. Intelligent Synthesis: Generates content based on question type and user needs
3. Adaptive Refinement: Applies appropriate formatting for the chosen response style

This service uses the interface-based architecture to support multiple LLM providers.
"""

import logging
from typing import List, Optional
from dataclasses import dataclass

# Import the ExtractedContent model from the API layer
# Using a forward reference to avoid circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..api.v1.models import ExtractedContent

from .interfaces.llm_interface import (
    LLMRequest,
    LLMResponse as BaseLLMResponse,
)
from .providers.gemini_2_0_flash_provider import GeminiLLMProvider
from .prompts import get_prompt

logger = logging.getLogger(__name__)


@dataclass
class QuestionAnalysis:
    """Result of question analysis stage."""
    question_type: str  # FACTUAL, EXPLANATORY, COMPARATIVE, COMPREHENSIVE
    detail_level: str   # LOW, MEDIUM, HIGH
    recommended_format: str  # CONCISE_TEXT, LISTS, TABLES, DETAILED_EXPLANATION
    reasoning: str
    search_enhancement: str  # Enhanced search query for better web results
    source_priorities: str   # Types of sources to prioritize
    special_considerations: str


class IntelligentLLMSynthesisService:
    """Service for intelligent, question-aware answer synthesis using Large Language Models."""

    def __init__(self) -> None:
        self.llm_provider: Optional[GeminiLLMProvider]
        """Initialize the intelligent LLM synthesis service."""
        import os

        api_key = os.getenv("GOOGLE_AI_API_KEY")
        if api_key:
            self.llm_provider = GeminiLLMProvider(api_key=api_key)

            if not self.llm_provider.is_configured():
                logger.warning(
                    "Google Gemini provider not configured"
                )
        else:
            logger.warning(
                "No GOOGLE_AI_API_KEY environment variable found"
            )
            self.llm_provider = None

    async def synthesize_answer(
        self, query: str, extracted_content: List["ExtractedContent"]
    ) -> "BaseLLMResponse":
        """
        Synthesize an intelligent, question-aware answer based on user query and extracted web content.

        Args:
            query: The user's search query
            extracted_content: List of extracted content from web pages

        Returns:
            LLMResponse containing the synthesized answer or error information
        """
        try:
            if not self.llm_provider or not self.llm_provider.is_configured():
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="Google Gemini provider not properly configured",
                )

            if not extracted_content:
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="No content available for synthesis",
                )

            # Filter successful extractions
            successful_content = [
                content
                for content in extracted_content
                if content.success
            ]

            if not successful_content:
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="No successful content extractions available",
                )

            # Combine extracted content
            combined_content = self._combine_extracted_content(
                successful_content
            )

            # Stage 1: Question Analysis for Response Strategy
            logger.info("🧠 Starting Stage 1: Question Analysis")
            question_analysis = await self._analyze_question(query)
            
            if not question_analysis:
                logger.error("❌ Question analysis failed")
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="Question analysis failed",
                )

            logger.info(
                f"✅ Stage 1 completed. Question type: {question_analysis.question_type}, "
                f"Detail level: {question_analysis.detail_level}, "
                f"Format: {question_analysis.recommended_format}"
            )

            # Stage 2: Intelligent Synthesis Based on Analysis
            logger.info("🎯 Starting Stage 2: Intelligent Synthesis")
            synthesis_response = await self._intelligent_synthesis(
                query, combined_content, question_analysis
            )

            if not synthesis_response or not synthesis_response.success:
                logger.error("❌ Intelligent synthesis failed")
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="Intelligent synthesis failed",
                )

            logger.info(
                f"✅ Stage 2 completed. Response length: {len(synthesis_response.content) if synthesis_response.content else 0} characters"
            )

            # Stage 3: Adaptive Refinement for Optimal Presentation
            logger.info("✨ Starting Stage 3: Adaptive Refinement")
            final_response = await self._adaptive_refinement(
                query, synthesis_response.content, question_analysis
            )

            if not final_response or not final_response.success:
                logger.error("❌ Adaptive refinement failed")
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="Adaptive refinement failed",
                )

            logger.info(
                f"✅ Stage 3 completed. Final response length: {len(final_response.content) if final_response.content else 0} characters"
            )
            logger.info(
                f"🎯 Intelligent three-stage LLM response completed: success={final_response.success}, "
                f"content_length={len(final_response.content) if final_response.content else 0}"
            )

            return final_response

        except Exception as e:
            logger.error(f"❌ Error in intelligent LLM synthesis: {str(e)}")
            return BaseLLMResponse(
                content="",
                success=False,
                error_message=f"Intelligent synthesis error: {str(e)}",
            )

    async def _analyze_question(self, query: str) -> Optional[QuestionAnalysis]:
        """
        Analyze the user's question to determine optimal response strategy.

        Args:
            query: The user's search query

        Returns:
            QuestionAnalysis object with response strategy recommendations
        """
        try:
            analysis_prompt = self._create_question_analysis_prompt(query)
            
            analysis_request = LLMRequest(
                prompt=analysis_prompt,
                system_message=get_prompt("question_analysis"),
            )

            analysis_response = await self.llm_provider.generate_response(
                analysis_request
            )

            if not analysis_response or not analysis_response.success:
                logger.error("Question analysis LLM call failed")
                return None

            # Parse the analysis response to extract structured information
            analysis = self._parse_question_analysis(analysis_response.content)
            return analysis

        except Exception as e:
            logger.error(f"Error in question analysis: {str(e)}")
            return None

    async def _intelligent_synthesis(
        self, 
        query: str, 
        content: str, 
        analysis: QuestionAnalysis
    ) -> Optional["BaseLLMResponse"]:
        """
        Perform intelligent synthesis based on question analysis.

        Args:
            query: The user's search query
            content: Combined extracted content from web sources
            analysis: Question analysis results

        Returns:
            LLMResponse with synthesized content
        """
        try:
            synthesis_prompt = self._create_intelligent_synthesis_prompt(
                query, content, analysis
            )

            synthesis_request = LLMRequest(
                prompt=synthesis_prompt,
                system_message=get_prompt("intelligent_synthesis"),
            )

            synthesis_response = await self.llm_provider.generate_response(
                synthesis_request
            )

            return synthesis_response

        except Exception as e:
            logger.error(f"Error in intelligent synthesis: {str(e)}")
            return None

    async def _adaptive_refinement(
        self, 
        query: str, 
        content: str, 
        analysis: QuestionAnalysis
    ) -> Optional["BaseLLMResponse"]:
        """
        Perform adaptive refinement based on question analysis.

        Args:
            query: The user's search query
            content: Synthesized content from previous stage
            analysis: Question analysis results

        Returns:
            LLMResponse with refined content
        """
        try:
            refinement_prompt = self._create_adaptive_refinement_prompt(
                query, content, analysis
            )

            refinement_request = LLMRequest(
                prompt=refinement_prompt,
                system_message=get_prompt("adaptive_refinement"),
            )

            refinement_response = await self.llm_provider.generate_response(
                refinement_request
            )

            return refinement_response

        except Exception as e:
            logger.error(f"Error in adaptive refinement: {str(e)}")
            return None

    def _create_question_analysis_prompt(self, query: str) -> str:
        """
        Create a prompt for question analysis.

        Args:
            query: User's search query

        Returns:
            Formatted prompt for question analysis
        """
        prompt = f"""Analyze this user question to determine the optimal response format, detail level, AND search strategy:

User Question: {query}

Please provide your analysis in the following format:

**Question Type:** [FACTUAL/EXPLANATORY/COMPARATIVE/COMPREHENSIVE]

**Detail Level:** [LOW/MEDIUM/HIGH]

**Recommended Format:** [CONCISE_TEXT/LISTS/TABLES/DETAILED_EXPLANATION]

**Reasoning:** [Brief explanation of why this format is optimal]

**Search Enhancement:** [Enhanced search query for better web results]

**Source Priorities:** [Types of sources to prioritize for this question]

**Special Considerations:** [Any unique aspects that affect response format or search strategy]

Analysis:"""

        return prompt

    def _create_intelligent_synthesis_prompt(
        self, 
        query: str, 
        content: str, 
        analysis: QuestionAnalysis
    ) -> str:
        """
        Create a prompt for intelligent synthesis based on question analysis.

        Args:
            query: User's search query
            content: Combined extracted content from web sources
            analysis: Question analysis results

        Returns:
            Formatted prompt for intelligent synthesis
        """
        prompt = f"""User Question: {query}

Question Analysis:
- Type: {analysis.question_type}
- Detail Level: {analysis.detail_level}
- Recommended Format: {analysis.recommended_format}
- Reasoning: {analysis.reasoning}
- Search Enhancement: {analysis.search_enhancement}
- Source Priorities: {analysis.source_priorities}

Provided Source Material:
{content}

Please provide an answer that:
1. Directly answers the user's question
2. Uses the recommended format and detail level
3. Is based ONLY on the provided source material
4. Includes proper source citations [1], [2], [3] for all information
5. Matches the user's actual needs (concise for simple questions, detailed for complex ones)

**Format Guidelines:**
- For FACTUAL questions: Provide a direct, concise answer
- For EXPLANATORY questions: Clear explanation with key points
- For COMPARATIVE questions: Structured comparison with tables if beneficial
- For COMPREHENSIVE questions: Organized, comprehensive coverage

**Note:** The search was optimized using: "{analysis.search_enhancement}"
**Source Priority:** {analysis.source_priorities}

Answer:"""

        return prompt

    def _create_adaptive_refinement_prompt(
        self, 
        query: str, 
        content: str, 
        analysis: QuestionAnalysis
    ) -> str:
        """
        Create a prompt for adaptive refinement based on question analysis.

        Args:
            query: User's search query
            content: Synthesized content from previous stage
            analysis: Question analysis results

        Returns:
            Formatted prompt for adaptive refinement
        """
        prompt = f"""User Question: {query}

Question Analysis:
- Type: {analysis.question_type}
- Detail Level: {analysis.detail_level}
- Recommended Format: {analysis.recommended_format}
- Search Enhancement: {analysis.search_enhancement}
- Source Priorities: {analysis.source_priorities}

Content to Refine:
{content}

Please refine this content to:
1. Ensure the format matches the question type and user needs
2. Apply appropriate markdown formatting (headers, lists, tables)
3. Maintain all information and source citations
4. Improve readability and organization
5. Use only proper markdown syntax (no HTML)

**Formatting Requirements:**
- For FACTUAL questions: Clean, simple presentation
- For EXPLANATORY questions: Clear structure with bullet points
- For COMPARATIVE questions: Well-structured tables when beneficial
- For COMPREHENSIVE questions: Logical section organization

**Markdown Rules:**
- Use ## for major sections, ### for subsections
- Use - for unordered lists, 1. for ordered lists
- Use | characters for tables with proper borders
- Use **bold** for key terms and concepts
- Use double line breaks for spacing
- NEVER use HTML tags

**Search Context:** This response was generated using search optimized for: "{analysis.search_enhancement}"
**Source Focus:** Prioritized sources: {analysis.source_priorities}

Refined Content:"""

        return prompt

    def _parse_question_analysis(self, analysis_text: str) -> QuestionAnalysis:
        """
        Parse the LLM response to extract structured question analysis.

        Args:
            analysis_text: Raw LLM response from question analysis

        Returns:
            QuestionAnalysis object with parsed information
        """
        try:
            # Default values
            question_type = "EXPLANATORY"
            detail_level = "MEDIUM"
            recommended_format = "DETAILED_EXPLANATION"
            reasoning = "Default analysis"
            search_enhancement = "None"
            source_priorities = "All"
            special_considerations = "None"

            # Parse the response text to extract structured information
            lines = analysis_text.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith("**Question Type:**"):
                    question_type = line.replace("**Question Type:**", "").strip().strip("[]")
                elif line.startswith("**Detail Level:**"):
                    detail_level = line.replace("**Detail Level:**", "").strip().strip("[]")
                elif line.startswith("**Recommended Format:**"):
                    recommended_format = line.replace("**Recommended Format:**", "").strip().strip("[]")
                elif line.startswith("**Reasoning:**"):
                    reasoning = line.replace("**Reasoning:**", "").strip()
                elif line.startswith("**Search Enhancement:**"):
                    search_enhancement = line.replace("**Search Enhancement:**", "").strip()
                elif line.startswith("**Source Priorities:**"):
                    source_priorities = line.replace("**Source Priorities:**", "").strip()
                elif line.startswith("**Special Considerations:**"):
                    special_considerations = line.replace("**Special Considerations:**", "").strip()

            return QuestionAnalysis(
                question_type=question_type,
                detail_level=detail_level,
                recommended_format=recommended_format,
                reasoning=reasoning,
                search_enhancement=search_enhancement,
                source_priorities=source_priorities,
                special_considerations=special_considerations
            )

        except Exception as e:
            logger.error(f"Error parsing question analysis: {str(e)}")
            # Return default analysis
            return QuestionAnalysis(
                question_type="EXPLANATORY",
                detail_level="MEDIUM",
                recommended_format="DETAILED_EXPLANATION",
                reasoning="Default analysis due to parsing error",
                search_enhancement="None",
                source_priorities="All",
                special_considerations="None"
            )

    def _combine_extracted_content(
        self, extracted_content: List["ExtractedContent"]
    ) -> str:
        """
        Combine extracted content from multiple sources into a single string.

        Args:
            extracted_content: List of successfully extracted content

        Returns:
            Combined content string with source attribution
        """
        combined = []
        
        for i, content in enumerate(extracted_content, 1):
            if content.extracted_text:
                # Add source identifier
                source_info = f"[Source {i}]"
                if content.url:
                    source_info += f" {content.url}"
                
                combined.append(f"{source_info}\n{content.extracted_text}\n")
        
        return "\n".join(combined)
