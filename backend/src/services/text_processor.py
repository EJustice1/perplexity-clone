"""
Search service layer.
Contains business logic for search operations.
"""


class SearchService:
    """Service class for search operations."""

    @staticmethod
    def search(query: str) -> str:
        """
        Process search query with a simple passthrough response.

        Args:
            query: The search query to process

        Returns:
            A simple response indicating what was searched for

        Raises:
            ValueError: If query is empty or invalid
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")

        # Simple passthrough response for now
        result = f"You searched for: {query.strip()}"

        return result

    @staticmethod
    def validate_query(query: str) -> bool:
        """
        Validate that search query meets processing requirements.

        Args:
            query: The query to validate

        Returns:
            True if query is valid, False otherwise
        """
        return query is not None and query.strip() != ""


# Global service instance
search_service = SearchService()
