"""
LLM Synthesis Service for generating AI-powered answers from extracted web content.

This service implements Retrieval-Augmented Generation (RAG) by combining user queries
with extracted web content to generate comprehensive, source-based answers.

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

from .interfaces.llm_interface import LLMRequest, LLMResponse as BaseLLMResponse
from .providers.gemini_llm_provider import GeminiLLMProvider

# Import the API model for the return type
from ..api.v1.models import LLMResponse

logger = logging.getLogger(__name__)


class LLMSynthesisService:
    """Service for synthesizing answers using Large Language Models."""
    
    def __init__(self):
        """Initialize the LLM synthesis service."""
        from ..core.config import sensitive_settings
        self.llm_provider = GeminiLLMProvider(
            api_key=sensitive_settings.google_ai_api_key
        )
        
        if not self.llm_provider.is_configured():
            logger.warning("Google Gemini provider not configured")
    
    async def synthesize_answer(
        self, 
        query: str, 
        extracted_content: List["ExtractedContent"]
    ) -> "LLMResponse":
        """
        Synthesize an answer based on user query and extracted web content.
        
        Args:
            query: The user's search query
            extracted_content: List of extracted content from web pages
            
        Returns:
            LLMResponse containing the synthesized answer or error information
        """
        try:
            if not self.llm_provider:
                return LLMResponse(
                    answer="",
                    success=False,
                    error_message="LLM provider not configured"
                )
            
            if not extracted_content:
                return LLMResponse(
                    answer="",
                    success=False,
                    error_message="No content available for synthesis"
                )
            
            # Filter successful extractions
            successful_content = [content for content in extracted_content if content.success]
            
            if not successful_content:
                return LLMResponse(
                    answer="",
                    success=False,
                    error_message="No successful content extractions available"
                )
            
            # Combine extracted content
            combined_content = self._combine_extracted_content(successful_content)
            
            # Create RAG prompt
            prompt = self._create_rag_prompt(query, combined_content)
            
            # Create LLM request
            llm_request = LLMRequest(
                prompt=prompt,
                system_message="You are a helpful AI assistant that answers questions based only on provided content."
            )
            
            # Call LLM provider
            llm_response = await self.llm_provider.generate_response(llm_request)
            
            # Convert interface response to API model format
            return LLMResponse(
                answer=llm_response.content,
                success=llm_response.success,
                error_message=llm_response.error_message,
                tokens_used=llm_response.tokens_used
            )
            
        except Exception as e:
            logger.error(f"Error in LLM synthesis: {str(e)}", exc_info=True)
            return LLMResponse(
                answer="",
                success=False,
                error_message=f"LLM synthesis failed: {str(e)}"
            )
    
    def _combine_extracted_content(self, content_list: List["ExtractedContent"]) -> str:
        """
        Combine extracted content from multiple sources into a single text.
        
        Args:
            content_list: List of extracted content objects
            
        Returns:
            Combined text content
        """
        combined_parts = []
        
        for i, content in enumerate(content_list, 1):
            # Add source identifier and content
            source_text = f"Source {i} ({content.title}):\n{content.extracted_text}\n"
            combined_parts.append(source_text)
        
        return "\n".join(combined_parts)
    
    def _create_rag_prompt(self, query: str, content: str) -> str:
        """
        Create a Retrieval-Augmented Generation prompt.
        
        Args:
            query: User's search query
            content: Combined extracted content from web sources
            
        Returns:
            Formatted prompt for the LLM
        """
        prompt = f"""Based ONLY on the provided text below, answer the user's question. 
Do not use any outside knowledge or information not present in the provided text.

User Question: {query}

Provided Text:
{content}

Instructions:
1. Answer the question using ONLY the information from the provided text above
2. If the provided text doesn't contain enough information to answer the question, say so clearly
3. Be comprehensive but concise
4. Cite specific sources when possible (e.g., "According to Source 1...")
5. Do not make up or infer information that isn't explicitly stated in the text

Answer:"""
        
        return prompt
    
    def is_configured(self) -> bool:
        """Check if the LLM service is properly configured."""
        return bool(self.llm_provider and self.llm_provider.is_configured())


def get_llm_synthesis_service() -> LLMSynthesisService:
    """Get an instance of the LLM synthesis service."""
    return LLMSynthesisService()
