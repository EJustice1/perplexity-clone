"""
Flask-specific metrics middleware implementation.
Provides sync middleware integration for Flask applications.
"""

import time
from typing import Any
from .base import MetricsMiddleware

class FlaskMetricsMiddleware(MetricsMiddleware):
    """Flask-specific metrics middleware with sync support."""
    
    def __init__(self, service_name: str, enabled: bool = True):
        super().__init__(service_name, enabled)
    
    def before_request(self, request) -> None:
        """Flask before_request handler for request timing."""
        request.start_time = time.time()
        self.logger.debug(f"Processing request: {request.method} {request.endpoint}")
    
    def after_request(self, request, response) -> Any:
        """Flask after_request handler for metrics collection."""
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

def create_flask_middleware(service_name: str, enabled: bool = True) -> FlaskMetricsMiddleware:
    """Create a Flask metrics middleware instance."""
    return FlaskMetricsMiddleware(service_name, enabled)
