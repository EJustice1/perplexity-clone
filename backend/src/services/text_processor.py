"""
Text processing service layer.
Contains business logic for text transformation operations.
"""


class TextProcessorService:
    """Service class for text processing operations."""

    @staticmethod
    def process_text(text: str) -> str:
        """
        Process text by adding exclamation points around it.

        Args:
            text: The input text to process

        Returns:
            The processed text with exclamation points

        Raises:
            ValueError: If text is empty or invalid
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Process the text by adding exclamation points
        processed_text = f"!! {text.strip()} !!"

        return processed_text

    @staticmethod
    def validate_text(text: str) -> bool:
        """
        Validate that text meets processing requirements.

        Args:
            text: The text to validate

        Returns:
            True if text is valid, False otherwise
        """
        return text is not None and text.strip() != ""


# Global service instance
text_processor_service = TextProcessorService()
