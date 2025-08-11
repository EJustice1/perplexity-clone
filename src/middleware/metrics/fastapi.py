"""
FastAPI-specific metrics middleware implementation.
Provides async middleware integration for FastAPI applications.
"""

import time
from .base import MetricsMiddleware

class FastAPIMetricsMiddleware(MetricsMiddleware):
    """FastAPI-specific metrics middleware with async support."""
    
    def __init__(self, service_name: str, enabled: bool = True):
        super().__init__(service_name, enabled)
    
    async def metrics_middleware(self, request, call_next):
        """FastAPI middleware function for metrics collection."""
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

def create_fastapi_middleware(service_name: str, enabled: bool = True) -> FastAPIMetricsMiddleware:
    """Create a FastAPI metrics middleware instance."""
    return FastAPIMetricsMiddleware(service_name, enabled)
