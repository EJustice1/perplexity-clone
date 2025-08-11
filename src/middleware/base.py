"""
Base middleware class providing common functionality and interfaces.
All middleware implementations should inherit from this base class.
"""

import time
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
from functools import wraps

class BaseMiddleware(ABC):
    """Base class for all middleware implementations."""
    
    def __init__(self, service_name: str, enabled: bool = True):
        self.service_name = service_name
        self.enabled = enabled
        self.logger = logging.getLogger(f"middleware.{self.__class__.__name__}.{service_name}")
        
        if self.enabled:
            self.logger.info(f"Initialized {self.__class__.__name__} for service: {service_name}")
        else:
            self.logger.info(f"Disabled {self.__class__.__name__} for service: {service_name}")
    
    @abstractmethod
    def process_request(self, request: Any) -> Any:
        """Process the incoming request. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def process_response(self, request: Any, response: Any) -> Any:
        """Process the outgoing response. Must be implemented by subclasses."""
        pass
    
    def is_enabled(self) -> bool:
        """Check if the middleware is enabled."""
        return self.enabled
    
    def enable(self) -> None:
        """Enable the middleware."""
        self.enabled = True
        self.logger.info(f"Enabled {self.__class__.__name__}")
    
    def disable(self) -> None:
        """Disable the middleware."""
        self.enabled = False
        self.logger.info(f"Disabled {self.__class__.__name__}")
    
    def get_config(self) -> Dict[str, Any]:
        """Get middleware configuration."""
        return {
            "name": self.__class__.__name__,
            "service": self.service_name,
            "enabled": self.enabled
        }

class MiddlewareChain:
    """Chain multiple middleware together for sequential processing."""
    
    def __init__(self, *middleware: BaseMiddleware):
        self.middleware = [m for m in middleware if m.is_enabled()]
        self.logger = logging.getLogger("middleware.chain")
        self.logger.info(f"Created middleware chain with {len(self.middleware)} enabled middleware")
    
    def process_request(self, request: Any) -> Any:
        """Process request through all middleware in sequence."""
        for middleware in self.middleware:
            try:
                request = middleware.process_request(request)
            except Exception as e:
                self.logger.error(f"Error in {middleware.__class__.__name__}: {e}")
                raise
        return request
    
    def process_response(self, request: Any, response: Any) -> Any:
        """Process response through all middleware in reverse sequence."""
        for middleware in reversed(self.middleware):
            try:
                response = middleware.process_response(request, response)
            except Exception as e:
                self.logger.error(f"Error in {middleware.__class__.__name__}: {e}")
                raise
        return response

def middleware_decorator(middleware_instance: BaseMiddleware):
    """Decorator to apply middleware to functions."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not middleware_instance.is_enabled():
                return func(*args, **kwargs)
            
            # Process request
            request = middleware_instance.process_request(args[0] if args else None)
            
            try:
                # Execute function
                result = func(*args, **kwargs)
                
                # Process response
                response = middleware_instance.process_response(request, result)
                return response
                
            except Exception as e:
                # Handle errors in middleware
                middleware_instance.logger.error(f"Error in function {func.__name__}: {e}")
                raise
        
        return wrapper
    return decorator
