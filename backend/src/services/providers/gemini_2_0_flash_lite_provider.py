"""
Ultra-Lightweight LLM Provider for Query Enhancement.

This provider uses the smallest, fastest, and cheapest LLM model available
to enhance search queries with minimal overhead and cost.
"""

import logging
import httpx
from typing import Optional
from ..interfaces.query_enhancement_interface import (
    QueryEnhancementInterface,
    QueryEnhancementRequest,
    QueryEnhancementResponse
)

logger = logging.getLogger(__name__)


class Gemini2FlashLiteProvider(QueryEnhancementInterface):
    """
    Google Gemini 2.0 Flash-Lite provider for query enhancement.
    
    This provider is optimized for:
    - Minimal token usage (< 50 tokens total)
    - Fast response times (< 2 seconds)
    - Low cost per enhancement
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the ultra-lightweight LLM provider.
        
        Args:
            api_key: API key for the LLM service
        """
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-2.0-flash-lite"  # Smallest, fastest model
        self.timeout = 5.0  # Very short timeout
        
        if not api_key or not api_key.strip():
            logger.warning("No API key provided for ultra-lightweight LLM provider")


    async def enhance_query(self, request: QueryEnhancementRequest) -> QueryEnhancementResponse:
        """
        Enhance a search query using ultra-lightweight LLM processing.
        
        Args:
            request: QueryEnhancementRequest with original query
            
        Returns:
            QueryEnhancementResponse with enhanced query
        """
        try:
            # Load the enhancement prompt from the prompts folder
            from ..prompts import get_prompt
            prompt_template = get_prompt("query_enhancement")
            prompt = prompt_template.format(query=request.original_query)
            
            # Minimal request payload
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "maxOutputTokens": request.max_response_tokens,
                    "temperature": 0.1,  # Very low for consistency
                    "topP": 0.8,
                    "topK": 1
                }
            }
            
            headers = {"Content-Type": "application/json"}
            params = {"key": self.api_key}
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/{self.model}:generateContent",
                    headers=headers,
                    params=params,
                    json=payload,
                    timeout=self.timeout
                )
                
                response.raise_for_status()
                data = response.json()
                
                # Extract enhanced query from response
                if "candidates" in data and data["candidates"]:
                    enhanced_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    enhanced_query = enhanced_text.strip()
                    
                    # Validate enhanced query
                    if enhanced_query and len(enhanced_query) > 0:
                        return QueryEnhancementResponse(
                            enhanced_query=enhanced_query,
                            success=True,
                            tokens_used=self._estimate_tokens(prompt, enhanced_text)
                        )
                
                # Fallback to original query if enhancement fails
                logger.warning("LLM enhancement failed, using original query")
                return QueryEnhancementResponse(
                    enhanced_query=request.original_query,
                    success=False,
                    error_message="Enhancement failed, using original query"
                )


        except httpx.TimeoutException:
            logger.warning("LLM enhancement timed out, using original query")
            return QueryEnhancementResponse(
                enhanced_query=request.original_query,
                success=False,
                error_message="Enhancement timed out, using original query"
            )
        except Exception as e:
            logger.error(f"LLM enhancement error: {str(e)}")
            return QueryEnhancementResponse(
                enhanced_query=request.original_query,
                success=False,
                error_message=f"Enhancement error: {str(e)}"
            )


    def is_configured(self) -> bool:
        """Check if the provider is properly configured."""
        return bool(self.api_key and self.api_key.strip())
    
    def get_provider_name(self) -> str:
        """Get the name of this provider."""
        return "gemini_2_0_flash_lite"


    def _estimate_tokens(self, prompt: str, response: str) -> int:
        """Rough token estimation for monitoring."""
        # Simple estimation: ~4 characters per token
        return len(prompt + response) // 4
