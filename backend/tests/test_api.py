"""
Integration tests for the FastAPI API endpoints.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock

# Add the src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test cases for the health endpoint."""

    def test_health_check_success(self):
        """Test successful health check."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["message"] == "API is running"
        assert "timestamp" in data

    def test_root_health_check_success(self):
        """Test successful root health check for load balancer."""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["message"] == "API is running"
        assert "timestamp" in data

    def test_health_check_methods(self):
        """Test health endpoint only accepts GET method."""
        response = client.post("/api/v1/health")
        assert response.status_code == 405

        response = client.put("/api/v1/health")
        assert response.status_code == 405


class TestSearchEndpoint:
    """Test cases for the search endpoint."""

    @patch("src.services.web_search.get_web_search_service")
    def test_search_success(self, mock_get_service):
        """Test successful search processing."""
        # Mock the web search service
        mock_service = MagicMock()
        mock_service.search = AsyncMock(
            return_value=[
                MagicMock(
                    title="Test Result",
                    url="https://example.com",
                    snippet="Test snippet",
                    source="web_search",
                )
            ]
        )
        # Mock the enhancement info
        mock_service.last_enhancement_info = {
            "original_query": "Hello World",
            "enhanced_query": "Hello World",
            "enhancement_success": False,
            "error_message": "Query enhancement disabled for testing"
        }
        mock_get_service.return_value = mock_service

        # Also mock the create function to prevent real service creation
        with patch(
            "src.services.web_search.create_web_search_service",
            return_value=mock_service,
        ):
            response = client.post(
                "/api/v1/search", json={"query": "Hello World"}
            )
            assert response.status_code == 200

            data = response.json()
            assert "sources" in data
            assert len(data["sources"]) == 1

    def test_search_empty_string(self):
        """Test search with empty string."""
        response = client.post("/api/v1/search", json={"query": ""})
        assert response.status_code == 400

        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Search query cannot be empty"

    @patch("src.services.web_search.get_web_search_service")
    def test_search_whitespace_only(self, mock_get_service):
        """Test search with whitespace-only string."""
        # Mock the web search service to return an error for empty queries
        mock_service = MagicMock()
        mock_service.search = AsyncMock(
            side_effect=ValueError("Search query cannot be empty")
        )
        mock_get_service.return_value = mock_service

        response = client.post(
            "/api/v1/search", json={"query": "   "}
        )
        assert response.status_code == 400

        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Search query cannot be empty"

    def test_search_missing_query_field(self):
        """Test search with missing query field."""
        response = client.post("/api/v1/search", json={})
        assert response.status_code == 422

    def test_search_invalid_json(self):
        """Test search with invalid JSON."""
        response = client.post(
            "/api/v1/search",
            content="invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422

    def test_search_methods(self):
        """Test search endpoint only accepts POST method."""
        response = client.get("/api/v1/search")
        assert response.status_code == 405

        response = client.put("/api/v1/search")
        assert response.status_code == 405

    @patch("src.services.web_search.get_web_search_service")
    def test_search_with_special_characters(self, mock_get_service):
        """Test search with special characters and numbers."""
        # Mock the web search service
        mock_service = MagicMock()
        mock_service.search = AsyncMock(
            return_value=[
                MagicMock(
                    title="Test Result",
                    url="https://example.com",
                    snippet="Test snippet",
                    source="web_search",
                )
            ]
        )
        # Mock the enhancement info
        mock_service.last_enhancement_info = {
            "original_query": "What is 2+2? & AI/ML",
            "enhanced_query": "What is 2+2? & AI/ML",
            "enhancement_success": False,
            "error_message": "Query enhancement disabled for testing"
        }
        mock_get_service.return_value = mock_service

        # Also mock the create function to prevent real service creation
        with patch(
            "src.services.web_search.create_web_search_service",
            return_value=mock_service,
        ):
            response = client.post(
                "/api/v1/search",
                json={"query": "What is 2+2? & AI/ML"},
            )
            assert response.status_code == 200

            data = response.json()
            assert "sources" in data
            assert len(data["sources"]) == 1

    @patch("src.services.web_search.get_web_search_service")
    def test_search_with_long_query(self, mock_get_service):
        """Test search with a longer query."""
        # Mock the web search service
        mock_service = MagicMock()
        mock_service.search = AsyncMock(
            return_value=[
                MagicMock(
                    title="Test Result",
                    url="https://example.com",
                    snippet="Test snippet",
                    source="web_search",
                )
            ]
        )
        # Mock the enhancement info
        mock_service.last_enhancement_info = {
            "original_query": "This is a very long search query that tests the system's ability to handle extended text input without any issues or problems",
            "enhanced_query": "This is a very long search query that tests the system's ability to handle extended text input without any issues or problems",
            "enhancement_success": False,
            "error_message": "Query enhancement disabled for testing"
        }
        mock_get_service.return_value = mock_service

        # Also mock the create function to prevent real service creation
        with patch(
            "src.services.web_search.create_web_search_service",
            return_value=mock_service,
        ):
            long_query = "This is a very long search query that tests the system's ability to handle extended text input without any issues or problems"
            response = client.post(
                "/api/v1/search", json={"query": long_query}
            )
            assert response.status_code == 200

            data = response.json()
            assert "sources" in data
            assert len(data["sources"]) == 1


class TestAPIRouting:
    """Test cases for API routing and structure."""

    def test_api_v1_prefix(self):
        """Test that API endpoints are properly prefixed."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200  # Should exist

        response = client.get("/health")
        assert (
            response.status_code == 200
        )  # Root health endpoint exists for load balancer

    def test_404_for_unknown_endpoints(self):
        """Test that unknown endpoints return 404."""
        response = client.get("/unknown")
        assert response.status_code == 404

        response = client.post("/api/v1/unknown")
        assert response.status_code == 404
