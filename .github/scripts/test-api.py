#!/usr/bin/env python3
"""
API Test Runner
This script reads the test configuration and runs all API tests dynamically.
Usage: python test-api.py <backend_url> <frontend_url> [dispatcher_url] [worker_url]
"""

import sys
import yaml
import requests
import subprocess
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class TestResult:
    """Represents the result of a test"""
    name: str
    success: bool
    message: str
    details: Optional[str] = None

class APITester:
    """Main API testing class"""
    
    def __init__(self, backend_url: str, frontend_url: str, dispatcher_url: Optional[str] = None, worker_url: Optional[str] = None):
        self.backend_url = backend_url.rstrip('/')
        self.frontend_url = frontend_url.rstrip('/')
        self.dispatcher_url = dispatcher_url.rstrip('/') if dispatcher_url else None
        self.worker_url = worker_url.rstrip('/') if worker_url else None
        self.config = self._load_config()
        self.results: list[TestResult] = []
        
    def _load_config(self) -> Dict[str, Any]:
        """Load test configuration from YAML file"""
        try:
            with open('.github/test-config.yml', 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print("❌ Test configuration file not found: .github/test-config.yml")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ Error parsing test configuration: {e}")
            sys.exit(1)
    
    def _get_auth_token(self) -> Optional[str]:
        """Get authentication token using gcloud"""
        try:
            result = subprocess.run(
                ['gcloud', 'auth', 'print-identity-token', '--audiences', self.backend_url],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Could not get auth token: {e}")
            return None
    
    def test_health_endpoint(self) -> TestResult:
        """Test the health endpoint"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=10)
            if response.status_code == 200:
                return TestResult(
                    name="Health Endpoint",
                    success=True,
                    message="Health endpoint working (200)",
                    details=f"Response: {response.text[:100]}..."
                )
            else:
                return TestResult(
                    name="Health Endpoint",
                    success=False,
                    message=f"Health endpoint failed with status: {response.status_code}",
                    details=f"Response: {response.text}"
                )
        except Exception as e:
            return TestResult(
                name="Health Endpoint",
                success=False,
                message=f"Health endpoint test failed: {str(e)}"
            )
    
    def test_search_endpoint_auth(self) -> TestResult:
        """Test the search endpoint with authentication"""
        try:
            token = self._get_auth_token()
            if not token:
                return TestResult(
                    name="Search Endpoint (Auth)",
                    success=False,
                    message="Could not get authentication token"
                )
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            data = {"query": "test"}
            # Search operations can take longer due to web search, content extraction, and LLM synthesis
            response = requests.post(
                f"{self.backend_url}/api/v1/search",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return TestResult(
                    name="Search Endpoint (Auth)",
                    success=True,
                    message="Search endpoint working (200)",
                    details=f"Response: {response.text}"
                )
            else:
                return TestResult(
                    name="Search Endpoint (Auth)",
                    success=False,
                    message=f"Search endpoint failed with status: {response.status_code}",
                    details=f"Response: {response.text}"
                )
        except Exception as e:
            return TestResult(
                name="Search Endpoint (Auth)",
                success=False,
                message=f"Search endpoint test failed: {str(e)}"
            )
    
    def test_cors_functionality(self) -> TestResult:
        """Test CORS functionality"""
        try:
            # Test CORS preflight request
            token = self._get_auth_token()
            access_request_headers = ["Content-Type"]
            if token:
                access_request_headers.append("Authorization")

            headers = {
                "Origin": self.frontend_url,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": ",".join(access_request_headers)
            }
            
            response = requests.options(
                f"{self.backend_url}/api/v1/search",
                headers=headers,
                timeout=10
            )
            
            cors_headers = response.headers.get('access-control-allow-origin')
            if cors_headers:
                cors_status = "✅ CORS preflight working"
            else:
                cors_status = "⚠️  CORS preflight may have issues"
            
            headers = {
                "Origin": self.frontend_url,
                "Content-Type": "application/json"
            }
            if token:
                headers["Authorization"] = f"Bearer {token}"
            
            data = {"query": "pipeline-test"}
            # Search operations can take longer due to web search, content extraction, and LLM synthesis
            response = requests.post(
                f"{self.backend_url}/api/v1/search",
                headers=headers,
                json=data
            )
            
            # Check if response matches expected pattern from config
            expected_pattern = self.config['api_endpoints']['search_cors']['success_pattern']
            if response.status_code == 200 and expected_pattern in response.text:
                return TestResult(
                    name="CORS Functionality",
                    success=True,
                    message=f"{cors_status}, API call with CORS working",
                    details=f"Response: {response.text}"
                )
            else:
                return TestResult(
                    name="CORS Functionality",
                    success=False,
                    message=f"{cors_status}, API call with CORS failed",
                    details=f"Status: {response.status_code}, Response: {response.text}"
                )
        except Exception as e:
            return TestResult(
                name="CORS Functionality",
                success=False,
                message=f"CORS test failed: {str(e)}"
            )
    
    def test_error_handling(self) -> TestResult:
        """Test error handling with invalid input"""
        try:
            headers = {"Content-Type": "application/json"}
            data = {"query": ""}
            
            response = requests.post(
                f"{self.backend_url}/api/v1/search",
                headers=headers,
                json=data,
                timeout=10
            )
            
            # Check if response matches expected pattern from config
            expected_pattern = self.config['api_endpoints']['search_error']['success_pattern']
            if response.status_code == 400 and expected_pattern in response.text:
                return TestResult(
                    name="Error Handling",
                    success=True,
                    message="Error handling working correctly",
                    details=f"Response: {response.text}"
                )
            else:
                return TestResult(
                    name="Error Handling",
                    success=False,
                    message=f"Error handling failed",
                    details=f"Expected 400, got {response.status_code}. Response: {response.text}"
                )
        except Exception as e:
            return TestResult(
                name="Error Handling",
                success=False,
                message=f"Error handling test failed: {str(e)}"
            )
    
    def test_dispatcher_endpoint(self) -> Optional[TestResult]:
        """Trigger dispatcher smoke endpoint when URL provided."""
        if not self.dispatcher_url:
            return None
        try:
            response = requests.post(f"{self.dispatcher_url}/dispatcher/dispatch", timeout=15)
            return TestResult(
                name="Dispatcher Trigger",
                success=response.status_code == 204,
                message=f"Dispatcher returned {response.status_code}",
                details=response.text[:100] if response.text else None,
            )
        except Exception as exc:
            return TestResult(
                name="Dispatcher Trigger",
                success=False,
                message=f"Dispatcher request failed: {exc}",
            )

    def test_worker_placeholder(self) -> Optional[TestResult]:
        """Placeholder for future worker tests."""
        if not self.worker_url:
            return None
        return TestResult(
            name="Worker Placeholder",
            success=True,
            message="Worker tests not implemented",
        )
    
    def run_all_tests(self) -> bool:
        """Run all configured tests"""
        print("🚀 Starting comprehensive API testing...")
        print(f"Backend URL: {self.backend_url}")
        print(f"Frontend URL: {self.frontend_url}")
        print(f"📋 Loaded test configuration from .github/test-config.yml")
        print()
        
        # Run all tests
        tests = [
            self.test_health_endpoint,
            self.test_search_endpoint_auth,
            self.test_cors_functionality,
            self.test_error_handling
        ]
        
        for test_func in tests:
            result = test_func()
            self.results.append(result)
            
            # Print result
            if result.success:
                print(f"✅ {result.name}: {result.message}")
            else:
                print(f"❌ {result.name}: {result.message}")
            
            if result.details:
                print(f"   Details: {result.details}")
            print()
        
        # Summary
        passed = sum(1 for r in self.results if r.success)
        total = len(self.results)
        
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All API tests passed successfully!")
            return True
        else:
            print("❌ Some tests failed. Check the details above.")
            return False

def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python test-api.py <backend_url> <frontend_url> [dispatcher_url] [worker_url]")
        sys.exit(1)
    
    backend_url = sys.argv[1]
    frontend_url = sys.argv[2]
    
    # Optional arguments for dispatcher and worker URLs
    dispatcher_url = None
    worker_url = None
    if len(sys.argv) > 3:
        dispatcher_url = sys.argv[3]
    if len(sys.argv) > 4:
        worker_url = sys.argv[4]
    
    tester = APITester(backend_url, frontend_url, dispatcher_url, worker_url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
