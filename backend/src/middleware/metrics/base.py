"""
Base metrics middleware implementation.
Provides common metrics collection functionality for all framework implementations.
"""

import time
from typing import Any
from ..base import BaseMiddleware

class MetricsMiddleware(BaseMiddleware):
    """Base metrics middleware implementation with common functionality."""
    
    def __init__(self, service_name: str, enabled: bool = True):
        super().__init__(service_name, enabled)
        self.request_start_times = {}
    
    def record_request_metrics(self, method: str, endpoint: str, status_code: int, duration: float) -> None:
        """Record standardized request metrics for monitoring."""
        try:
            from .utils import REQUEST_COUNT, REQUEST_LATENCY
            
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
        """Process incoming request - record start time for duration calculation."""
        if hasattr(request, 'start_time'):
            request.start_time = time.time()
        return request
    
    def process_response(self, request: Any, response: Any) -> Any:
        """Process outgoing response - record metrics and duration."""
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
