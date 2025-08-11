"""
Utility functions and global metrics for the metrics middleware package.
Contains Prometheus metrics definitions and helper functions.
"""

import time
from typing import Dict, Any
from prometheus_client import Counter, Histogram, CONTENT_TYPE_LATEST, generate_latest

# Global metrics - shared across all services
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP requests', 
    ['method', 'endpoint', 'status', 'service']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 
    'HTTP request latency',
    ['service']
)

def get_metrics_response() -> tuple:
    """Generate standardized Prometheus metrics response for both frameworks."""
    try:
        content = generate_latest()
        return content, CONTENT_TYPE_LATEST
    except Exception as e:
        raise RuntimeError(f"Error generating metrics: {e}")

def get_health_response(service_name: str) -> Dict[str, Any]:
    """Generate standardized health check response for both frameworks."""
    return {
        "status": "healthy", 
        "service": service_name,
        "timestamp": time.time()
    }
