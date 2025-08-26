"""
Custom middleware for request logging and monitoring.
Provides structured logging for all API requests.
"""

import time
import logging
import asyncio
from typing import Callable, Awaitable
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware that logs request information including method, path,
    status code, and processing time.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        # Record start time
        start_time = time.time()

        # Get request details
        method = request.method
        path = request.url.path
        query_params = (
            str(request.query_params) if request.query_params else ""
        )

        # Process the request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Get response details
        status_code = response.status_code

        # Log the request information
        logger.info(
            f"Request: {method} {path}"
            f"{'?' + query_params if query_params else ''} "
            f"| Status: {status_code} | Time: {process_time:.4f}s"
        )

        return response


class TimeoutMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds a timeout to all requests to prevent hanging.
    """

    def __init__(self, app, timeout_seconds: int = 120):
        super().__init__(app)
        self.timeout_seconds = timeout_seconds

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        try:
            # Add timeout to the request processing
            response = await asyncio.wait_for(
                call_next(request), 
                timeout=self.timeout_seconds
            )
            return response
        except asyncio.TimeoutError:
            logger.error(f"Request timeout after {self.timeout_seconds} seconds: {request.method} {request.url.path}")
            raise HTTPException(
                status_code=408, 
                detail=f"Request timeout after {self.timeout_seconds} seconds"
            )
