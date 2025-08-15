"""
Integration tests for the FastAPI API endpoints.
"""

import pytest
import sys
import os
from pathlib import Path

# Add the src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from main import app

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


class TestTextProcessingEndpoint:
    """Test cases for the text processing endpoint."""
    
    def test_process_text_success(self):
        """Test successful text processing."""
        response = client.post(
            "/api/v1/process-text",
            json={"text": "Hello World"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["result"] == "!! Hello World !!"
        
    def test_process_text_empty_string(self):
        """Test text processing with empty string."""
        response = client.post(
            "/api/v1/process-text",
            json={"text": ""}
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
        
    def test_process_text_whitespace_only(self):
        """Test text processing with whitespace-only string."""
        response = client.post(
            "/api/v1/process-text",
            json={"text": "   "}
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
        
    def test_process_text_missing_text_field(self):
        """Test text processing with missing text field."""
        response = client.post(
            "/api/v1/process-text",
            json={}
        )
        assert response.status_code == 422
        
    def test_process_text_invalid_json(self):
        """Test text processing with invalid JSON."""
        response = client.post(
            "/api/v1/process-text",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
        
    def test_process_text_methods(self):
        """Test text processing endpoint only accepts POST method."""
        response = client.get("/api/v1/process-text")
        assert response.status_code == 405
        
        response = client.put("/api/v1/process-text")
        assert response.status_code == 405


class TestAPIRouting:
    """Test cases for API routing and structure."""
    
    def test_api_v1_prefix(self):
        """Test that API endpoints are properly prefixed."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200  # Should exist
        
        response = client.get("/health")
        assert response.status_code == 200  # Root health endpoint exists for load balancer
        
    def test_404_for_unknown_endpoints(self):
        """Test that unknown endpoints return 404."""
        response = client.get("/unknown")
        assert response.status_code == 404
        
        response = client.post("/api/v1/unknown")
        assert response.status_code == 404
