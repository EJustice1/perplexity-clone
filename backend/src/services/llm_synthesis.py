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
from .providers.gemini_2_0_flash_provider import GeminiLLMProvider
from .prompts import get_prompt

logger = logging.getLogger(__name__)


class LLMSynthesisService:
    """Service for synthesizing answers using Large Language Models."""
    
    def __init__(self):
        """Initialize the LLM synthesis service."""
        import os
        api_key = os.getenv("GOOGLE_AI_API_KEY")
        if api_key:
            self.llm_provider = GeminiLLMProvider(api_key=api_key)
            
            if not self.llm_provider.is_configured():
                logger.warning("Google Gemini provider not configured")
        else:
            logger.warning("No GOOGLE_AI_API_KEY environment variable found")
            self.llm_provider = None
    
    async def synthesize_answer(
        self, 
        query: str, 
        extracted_content: List["ExtractedContent"]
    ) -> "BaseLLMResponse":
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
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="LLM provider not configured"
                )
            
            if not extracted_content:
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="No content available for synthesis"
                )
            
            # Filter successful extractions
            successful_content = [content for content in extracted_content if content.success]
            
            if not successful_content:
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="No successful content extractions available"
                )
            
            # Combine extracted content
            combined_content = self._combine_extracted_content(successful_content)
            
            # Stage 1: Initial Synthesis for Pure Information Accuracy
            logger.info("🚀 Starting Stage 1: Initial Synthesis")
            initial_prompt = self._create_initial_synthesis_prompt(query, combined_content)
            logger.info(f"📝 Initial synthesis prompt length: {len(initial_prompt)} characters")
            
            initial_llm_request = LLMRequest(
                prompt=initial_prompt,
                system_message=get_prompt('initial_synthesis')
            )
            logger.info(f"🔧 Initial synthesis system message length: {len(initial_llm_request.system_message)} characters")
            
            # Get initial synthesis response
            initial_response = await self.llm_provider.generate_response(initial_llm_request)
            
            if not initial_response or not initial_response.success:
                logger.error("❌ Initial synthesis failed")
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="Initial information synthesis failed"
                )
            
            logger.info(f"✅ Stage 1 completed. Response length: {len(initial_response.content) if initial_response.content else 0} characters")
            logger.info(f"📋 Stage 1 response preview: {initial_response.content[:200] if initial_response.content else 'None'}...")
            
            # Stage 2: Formatting Refinement for Professional Presentation
            logger.info("🎨 Starting Stage 2: Formatting Refinement")
            refinement_prompt = self._create_refinement_prompt(query, initial_response.content)
            logger.info(f"📝 Refinement prompt length: {len(refinement_prompt)} characters")
            
            refinement_llm_request = LLMRequest(
                prompt=refinement_prompt,
                system_message=get_prompt('formatting_refinement')
            )
            logger.info(f"🔧 Refinement system message length: {len(refinement_llm_request.system_message)} characters")
            
            # Get final formatted response
            final_response = await self.llm_provider.generate_response(refinement_llm_request)
            
            # Validate the final response before returning
            if not final_response:
                logger.error("❌ Formatting refinement failed")
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="Formatting refinement failed"
                )
            
            if not hasattr(final_response, 'content') or not hasattr(final_response, 'success'):
                logger.error(f"❌ Final response missing required fields. Response type: {type(final_response)}")
                return BaseLLMResponse(
                    content="",
                    success=False,
                    error_message="Final response missing required fields"
                )
            
            logger.info(f"✅ Stage 2 completed. Final response length: {len(final_response.content) if final_response.content else 0} characters")
            logger.info(f"📋 Final response preview: {final_response.content[:200] if final_response.content else 'None'}...")
            logger.info(f"🎯 Two-stage LLM response completed: success={final_response.success}, content_length={len(final_response.content) if final_response.content else 0}")
            
            # Check if tables are present in the final response
            if final_response.content:
                has_tables = '|' in final_response.content and '-' in final_response.content
                logger.info(f"📊 Final response contains tables: {has_tables}")
                if has_tables:
                    table_count = final_response.content.count('|---------')
                    logger.info(f"📊 Number of table separators found: {table_count}")
            
            # Return the validated final response
            return final_response
            
        except Exception as e:
            logger.error(f"Error in LLM synthesis: {str(e)}", exc_info=True)
            return BaseLLMResponse(
                content="",
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
    
    def _create_initial_synthesis_prompt(self, query: str, content: str) -> str:
        """
        Create a prompt for the initial synthesis stage.
        
        Args:
            query: User's search query
            content: Combined extracted content from web sources
            
        Returns:
            Formatted prompt for the initial synthesis
        """
        prompt = f"""User Question: {query}

Provided Source Material:
{content}

Please provide a comprehensive, consumer-friendly answer based ONLY on the information above. 

**Requirements:**
- Answer the user's question directly and completely
- Use proper source citations [1], [2], [3] for all information
- Format your response beautifully in markdown with headers, bullet points, and clear organization
- Be thorough and detailed without losing any important information
- Use simple, clear language that's easy to understand
- If the sources are insufficient, clearly state what information is missing

**Format your response in beautiful markdown with:**
- Clear headers (##) for major sections
- Bold text (**) for key concepts
- Bullet points for lists and examples
- Good paragraph breaks for readability

Answer:"""
        
        return prompt
    
    def _create_refinement_prompt(self, query: str, content: str) -> str:
        """
        Create a prompt for the formatting refinement stage.
        
        Args:
            query: User's search query
            content: Initial synthesized answer from the LLM
            
        Returns:
            Formatted prompt for the formatting refinement
        """
        prompt = f"""User Question: {query}

Initial Synthesized Answer:
{content}

CRITICAL: You MUST convert this information into professional tables with proper markdown syntax.

**MANDATORY TABLE REQUIREMENTS:**
- Use | characters to separate columns
- Use - characters for table separators (e.g., |---------|-------------|)
- EVERY table row must start and end with | characters
- EVERY cell must be separated by | characters
- Include source citations inline with the content (e.g., "description [1]")

**REQUIRED OUTPUT FORMAT:**
**Direct Answer:**
[Format the direct answer clearly]

**Key Points:**

| Concept | Description |
|---------|-------------|
| **[Bold Term]** | [Description with inline citation] |
| **[Bold Term]** | [Description with inline citation] |

**Additional Information:**

| Category | Details |
|----------|---------|
| [Category] | [Information with inline citation] |
| [Category] | [Information with inline citation] |

**SPACING REQUIREMENTS:**
- Add blank lines between all sections
- Add blank lines between tables and other content
- Use generous spacing for readability
- Ensure visual breathing room throughout

**EXAMPLE OF CORRECT TABLE SYNTAX:**
| Concept | Description |
|---------|-------------|
| **Qubits** | Replace classical bits and can exist in superposition states [2] |
| **Superposition** | Allows quantum computers to process vast amounts of data at once [2] |

Now format the answer with proper tables, spacing, and markdown syntax:"""
        
        return prompt
    
    def is_configured(self) -> bool:
        """Check if the LLM service is properly configured."""
        return bool(self.llm_provider and self.llm_provider.is_configured())


def get_llm_synthesis_service() -> LLMSynthesisService:
    """Get an instance of the LLM synthesis service."""
    return LLMSynthesisService()
