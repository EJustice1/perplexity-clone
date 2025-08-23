"""
Google Gemini LLM Provider Implementation.

This is the single LLM provider for the system, using Google's Gemini models
through their API for answer synthesis.
"""

import logging
from typing import List, Optional

from ..interfaces.llm_interface import LLMProviderInterface, LLMRequest, LLMResponse

logger = logging.getLogger(__name__)


class GeminiLLMProvider(LLMProviderInterface):
    """Google Gemini implementation of the LLM provider interface."""

    # Supported Google Gemini models
    SUPPORTED_MODELS = [
        "gemini-pro",
        "gemini-1.5-pro", 
        "gemini-1.5-flash",
        "gemini-2.0-flash"
    ]

    DEFAULT_MODEL = "gemini-2.0-flash"
    DEFAULT_MAX_TOKENS = 2048
    DEFAULT_TEMPERATURE = 0.7

    def __init__(self, api_key: str, **kwargs):
        """
        Initialize the Google Gemini LLM provider.
        
        Args:
            api_key: Google AI API key
            **kwargs: Additional configuration options
        """
        self.api_key = api_key
        self.default_model = kwargs.get("default_model", self.DEFAULT_MODEL)
        self.default_max_tokens = kwargs.get("default_max_tokens", self.DEFAULT_MAX_TOKENS)
        self.default_temperature = kwargs.get("default_temperature", self.DEFAULT_TEMPERATURE)
        
        # Lazy import to avoid dependency issues if Google AI not installed
        self._client = None
        
        logger.info(f"Initialized Google Gemini provider with model: {self.default_model}")

    def _get_client(self):
        """Get or create Google AI client instance."""
        if self._client is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai
            except ImportError:
                raise ImportError("Google AI package not installed. Run: pip install google-generativeai")
        return self._client

    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """
        Generate a response using Google Gemini API.
        
        Args:
            request: LLM request containing prompt and configuration
            
        Returns:
            LLMResponse containing the generated content and metadata
        """
        try:
            if not self.is_configured():
                return LLMResponse(
                    content="",
                    success=False,
                    error_message="Google Gemini provider not properly configured",
                    provider="gemini"
                )

            genai = self._get_client()
            
            # Prepare request parameters
            model_name = request.model or self.default_model
            max_tokens = request.max_tokens or self.default_max_tokens
            temperature = request.temperature or self.default_temperature

            # Validate model
            if not self.validate_model(model_name):
                return LLMResponse(
                    content="",
                    success=False,
                    error_message=f"Model '{model_name}' not supported by Google Gemini provider",
                    provider="gemini"
                )

            # Create model instance
            model = genai.GenerativeModel(model_name)

            # Prepare prompt (combine system message with user prompt if provided)
            full_prompt = request.prompt
            if request.system_message:
                full_prompt = f"{request.system_message}\n\n{request.prompt}"

            logger.debug(f"Making Google Gemini API call with model: {model_name}")

            # Generate content
            response = model.generate_content(
                full_prompt,
                generation_config={
                    "max_output_tokens": max_tokens,
                    "temperature": temperature
                }
            )

            # Extract response data
            content = response.text
            # Google AI doesn't provide token usage in the same format
            tokens_used = None
            finish_reason = response.candidates[0].finish_reason.name if response.candidates else None

            logger.info(f"Google Gemini API call successful")

            return LLMResponse(
                content=content,
                success=True,
                tokens_used=tokens_used,
                model_used=model_name,
                provider="gemini",
                finish_reason=finish_reason
            )

        except ImportError as e:
            logger.error(f"Google AI package not available: {str(e)}")
            return LLMResponse(
                content="",
                success=False,
                error_message="Google AI package not installed",
                provider="gemini"
            )
        except Exception as e:
            logger.error(f"Google Gemini API error: {str(e)}", exc_info=True)
            return LLMResponse(
                content="",
                success=False,
                error_message=f"Google Gemini API error: {str(e)}",
                provider="gemini"
            )

    def is_configured(self) -> bool:
        """
        Check if the Google Gemini provider is properly configured.
        
        Returns:
            True if API key is present, False otherwise
        """
        return bool(self.api_key)

    def get_provider_name(self) -> str:
        """
        Get the name of the provider.
        
        Returns:
            String identifier for this provider
        """
        return "gemini"

    def get_supported_models(self) -> List[str]:
        """
        Get list of models supported by Google Gemini.
        
        Returns:
            List of supported Google Gemini model names
        """
        return self.SUPPORTED_MODELS.copy()

    def validate_model(self, model: str) -> bool:
        """
        Validate if a model is supported by Google Gemini.
        
        Args:
            model: Model name to validate
            
        Returns:
            True if model is supported, False otherwise
        """
        return model in self.SUPPORTED_MODELS
