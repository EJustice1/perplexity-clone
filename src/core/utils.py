"""
Common utilities and helper functions for the Perplexity Clone application.
This module provides shared functionality across all services.
"""

import time
import logging
from typing import Any, Dict, Optional
from functools import wraps

def setup_logging(service_name: str, log_level: str = "INFO") -> logging.Logger:
    """Set up standardized logging for a service."""
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Create console handler if none exists
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.getLogger(func.__module__).debug(
            f"Function {func.__name__} executed in {execution_time:.4f} seconds"
        )
        return result
    return wrapper

def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get a value from a dictionary with a default fallback."""
    return data.get(key, default)

def validate_port(port: int) -> bool:
    """Validate that a port number is within valid range."""
    return 1 <= port <= 65535

def validate_host(host: str) -> bool:
    """Validate that a host string is valid."""
    if host == "0.0.0.0" or host == "localhost" or host == "127.0.0.1":
        return True
    # Add more validation as needed
    return True

def format_bytes(bytes_value: int) -> str:
    """Format bytes into human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable format."""
    if seconds < 1:
        return f"{seconds * 1000:.1f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

class ServiceHealth:
    """Standardized service health checker."""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.checks = {}
    
    def add_check(self, name: str, check_func: callable) -> None:
        """Add a health check function."""
        self.checks[name] = check_func
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status."""
        status = {
            "status": "healthy",
            "service": self.service_name,
            "timestamp": time.time(),
            "checks": {}
        }
        
        overall_healthy = True
        
        for check_name, check_func in self.checks.items():
            try:
                check_result = check_func()
                status["checks"][check_name] = {
                    "status": "healthy" if check_result else "unhealthy",
                    "result": check_result
                }
                if not check_result:
                    overall_healthy = False
            except Exception as e:
                status["checks"][check_name] = {
                    "status": "error",
                    "error": str(e)
                }
                overall_healthy = False
        
        status["status"] = "healthy" if overall_healthy else "unhealthy"
        return status
