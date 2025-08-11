"""
Metrics middleware for collecting HTTP request metrics and performance data.
Provides standardized metrics collection for both FastAPI and Flask applications.
"""

import time
from typing import Any, Dict, Optional
from prometheus_client import Counter, Histogram, CONTENT_TYPE_LATEST, generate_latest

from .base import BaseMiddleware

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
    """Get standardized metrics response for both frameworks."""
    try:
        content = generate_latest()
        return content, CONTENT_TYPE_LATEST
    except Exception as e:
        raise RuntimeError(f"Error generating metrics: {e}")

def get_health_response(service_name: str) -> Dict[str, Any]:
    """Get standardized health response for both frameworks."""
    return {
        "status": "healthy", 
        "service": service_name,
        "timestamp": time.time()
    }

class MetricsMiddleware(BaseMiddleware):
    """Base metrics middleware implementation."""
    
    def __init__(self, service_name: str, enabled: bool = True):
        super().__init__(service_name, enabled)
        self.request_start_times = {}
    
    def record_request_metrics(self, method: str, endpoint: str, status_code: int, duration: float) -> None:
        """Record standardized request metrics."""
        try:
            REQUEST_COUNT.labels(
                method=method,
                endpoint=endpoint,
                status=status_code,
                service=self.service_name
            ).inc()
            
            REQUEST_LATENCY.labels(service=self.service_name).observe(duration)
            
            self.logger.debug(
                f"Recorded metrics: {method} {endpoint} {status_code} "
                f"({duration:.4f}s) for {self.service_name}"
            )
        except Exception as e:
            self.logger.error(f"Error recording metrics: {e}")
    
    def process_request(self, request: Any) -> Any:
        """Process incoming request - record start time."""
        if hasattr(request, 'start_time'):
            request.start_time = time.time()
        return request
    
    def process_response(self, request: Any, response: Any) -> Any:
        """Process outgoing response - record metrics."""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Extract request information based on framework
            method = getattr(request, 'method', 'UNKNOWN')
            endpoint = getattr(request, 'endpoint', getattr(request, 'url', {}).path if hasattr(request, 'url') else 'UNKNOWN')
            status_code = getattr(response, 'status_code', 200)
            
            # Record metrics
            self.record_request_metrics(method, endpoint, status_code, duration)
            
            self.logger.debug(
                f"Request completed: {method} {endpoint} "
                f"-> {status_code} ({duration:.4f}s)"
            )
        
        return response

class FastAPIMetricsMiddleware(MetricsMiddleware):
    """FastAPI-specific metrics middleware implementation."""
    
    def __init__(self, service_name: str, enabled: bool = True):
        super().__init__(service_name, enabled)
    
    async def metrics_middleware(self, request, call_next):
        """FastAPI middleware for metrics collection."""
        start_time = time.time()
        
        # Log request start
        self.logger.debug(f"Processing request: {request.method} {request.url.path}")
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Record metrics
            self.record_request_metrics(
                method=request.method,
                endpoint=request.url.path,
                status_code=response.status_code,
                duration=duration
            )
            
            self.logger.debug(
                f"Request completed: {request.method} {request.url.path} "
                f"-> {response.status_code} ({duration:.4f}s)"
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(
                f"Request failed: {request.method} {request.url.path} "
                f"after {duration:.4f}s: {e}"
            )
            raise

class FlaskMetricsMiddleware(MetricsMiddleware):
    """Flask-specific metrics middleware implementation."""
    
    def __init__(self, service_name: str, enabled: bool = True):
        super().__init__(service_name, enabled)
    
    def before_request(self, request) -> None:
        """Flask before_request handler."""
        request.start_time = time.time()
        self.logger.debug(f"Processing request: {request.method} {request.endpoint}")
    
    def after_request(self, request, response) -> Any:
        """Flask after_request handler."""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Record metrics
            self.record_request_metrics(
                method=request.method,
                endpoint=request.endpoint,
                status_code=response.status_code,
                duration=duration
            )
            
            self.logger.debug(
                f"Request completed: {request.method} {request.endpoint} "
                f"-> {response.status_code} ({duration:.4f}s)"
            )
        
        return response

# Convenience functions for common operations
def create_fastapi_middleware(service_name: str, enabled: bool = True) -> FastAPIMetricsMiddleware:
    """Create a FastAPI metrics middleware instance."""
    return FastAPIMetricsMiddleware(service_name, enabled)

def create_flask_middleware(service_name: str, enabled: bool = True) -> FlaskMetricsMiddleware:
    """Create a Flask metrics middleware instance."""
    return FlaskMetricsMiddleware(service_name, enabled)
