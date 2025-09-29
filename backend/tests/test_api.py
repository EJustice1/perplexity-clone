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

    @patch("src.api.v1.endpoints.MultiQuerySearchOrchestrator")
    @patch("src.api.v1.endpoints.AnswerSynthesizer")
    @patch("src.api.v1.endpoints.ContentCollator")
    @patch("src.api.v1.endpoints.LangChainClient")
    @patch("src.api.v1.endpoints.LangChainConfig")
    def test_search_success(self, mock_config_cls, mock_client_cls, mock_collator_cls, mock_synth_cls, mock_orchestrator_cls):
        """Test successful search processing using mocked pipeline components."""

        mock_config = MagicMock()
        mock_config.synthesis_model_name = "model"
        mock_config.synthesis_temperature = 0.1
        mock_config.synthesis_max_output_tokens = 128
        mock_config.get_gemini_api_key.return_value = "key"
        mock_config_cls.from_env.return_value = mock_config
        mock_config_cls.return_value = mock_config

        mock_client = MagicMock()
        mock_client.decompose_query.return_value = ["hello world"]
        mock_multi_search = MagicMock()
        mock_multi_search.per_query_outcomes = [
            MagicMock(results=[
                MagicMock(title="Result", url="https://example.com", snippet="Snippet")
            ])
        ]
        mock_multi_search.aggregated_urls = ["https://example.com"]
        mock_collation = MagicMock()
        mock_collation.documents = []
        mock_collation.summary.successes = 0
        mock_collation.summary.failures = 0
        mock_collation.summary.total_urls = 0
        mock_collation.summary.failure_details = []
        mock_synth_answer = MagicMock(answer="Answer", cited_urls=["https://example.com"])

        mock_client.generate_multi_search_plan = AsyncMock(return_value=mock_multi_search)
        mock_client.collate_content = AsyncMock(return_value=mock_collation)
        mock_client.synthesize_answer = AsyncMock(return_value=mock_synth_answer)

        mock_client_cls.return_value = mock_client
        mock_collator_cls.return_value = MagicMock()
        mock_orchestrator_cls.return_value = MagicMock()
        mock_synth_instance = MagicMock()
        mock_synth_cls.return_value = mock_synth_instance

        response = client.post("/api/v1/search", json={"query": "Hello World"})
        assert response.status_code == 200

        data = response.json()
        assert data["llm_answer"]["answer"] == "Answer"
        assert data["citations"] == ["https://example.com"]
        assert data["sub_queries"] == ["hello world"]

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

    @patch("src.api.v1.endpoints.MultiQuerySearchOrchestrator")
    @patch("src.api.v1.endpoints.AnswerSynthesizer")
    @patch("src.api.v1.endpoints.ContentCollator")
    @patch("src.api.v1.endpoints.LangChainClient")
    @patch("src.api.v1.endpoints.LangChainConfig")
    def test_search_with_special_characters(self, mock_config_cls, mock_client_cls, mock_collator_cls, mock_synth_cls, mock_orchestrator_cls):
        """Test search with special characters and numbers."""

        mock_config = MagicMock()
        mock_config.synthesis_model_name = "model"
        mock_config.synthesis_temperature = 0.1
        mock_config.synthesis_max_output_tokens = 128
        mock_config.get_gemini_api_key.return_value = None
        mock_config_cls.from_env.return_value = mock_config
        mock_config_cls.return_value = mock_config

        mock_client = MagicMock()
        mock_client.decompose_query.return_value = ["query"]
        mock_multi_search = MagicMock()
        mock_multi_search.per_query_outcomes = [
            MagicMock(results=[MagicMock(title="Result", url="https://example.com", snippet="Snippet")])
        ]
        mock_multi_search.aggregated_urls = []
        mock_collation = MagicMock()
        mock_collation.documents = []
        mock_collation.summary.successes = 0
        mock_collation.summary.failures = 0
        mock_collation.summary.total_urls = 0
        mock_collation.summary.failure_details = []

        mock_client.generate_multi_search_plan = AsyncMock(return_value=mock_multi_search)
        mock_client.collate_content = AsyncMock(return_value=mock_collation)
        mock_client.synthesize_answer = AsyncMock(return_value=None)

        mock_client_cls.return_value = mock_client
        mock_collator_cls.return_value = MagicMock()
        mock_orchestrator_cls.return_value = MagicMock()
        mock_synth_cls.return_value = MagicMock()

        response = client.post(
            "/api/v1/search",
            json={"query": "What is 2+2? & AI/ML"},
        )
        assert response.status_code == 200

        data = response.json()
        assert "sources" in data
        assert len(data["sources"]) == 1
        assert data["sub_queries"] == ["query"]

    @patch("src.api.v1.endpoints.MultiQuerySearchOrchestrator")
    @patch("src.api.v1.endpoints.AnswerSynthesizer")
    @patch("src.api.v1.endpoints.ContentCollator")
    @patch("src.api.v1.endpoints.LangChainClient")
    @patch("src.api.v1.endpoints.LangChainConfig")
    def test_search_with_long_query(self, mock_config_cls, mock_client_cls, mock_collator_cls, mock_synth_cls, mock_orchestrator_cls):
        """Test search with a longer query."""

        mock_config = MagicMock()
        mock_config.synthesis_model_name = "model"
        mock_config.synthesis_temperature = 0.1
        mock_config.synthesis_max_output_tokens = 128
        mock_config.get_gemini_api_key.return_value = None
        mock_config_cls.from_env.return_value = mock_config
        mock_config_cls.return_value = mock_config

        mock_client = MagicMock()
        mock_client.decompose_query.return_value = ["query"]
        mock_multi_search = MagicMock()
        mock_multi_search.per_query_outcomes = [
            MagicMock(results=[MagicMock(title="Result", url="https://example.com", snippet="Snippet")])
        ]
        mock_multi_search.aggregated_urls = []
        mock_collation = MagicMock()
        mock_collation.documents = []
        mock_collation.summary.successes = 0
        mock_collation.summary.failures = 0
        mock_collation.summary.total_urls = 0
        mock_collation.summary.failure_details = []

        mock_client.generate_multi_search_plan = AsyncMock(return_value=mock_multi_search)
        mock_client.collate_content = AsyncMock(return_value=mock_collation)
        mock_client.synthesize_answer = AsyncMock(return_value=None)

        mock_client_cls.return_value = mock_client
        mock_collator_cls.return_value = MagicMock()
        mock_orchestrator_cls.return_value = MagicMock()
        mock_synth_cls.return_value = MagicMock()

        long_query = "This is a very long search query that tests the system's ability to handle extended text input without any issues or problems"
        response = client.post("/api/v1/search", json={"query": long_query})
        assert response.status_code == 200

        data = response.json()
        assert "sources" in data
        assert len(data["sources"]) == 1
        assert data["sub_queries"] == ["query"]


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
