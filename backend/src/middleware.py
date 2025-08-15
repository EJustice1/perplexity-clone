"""
Custom middleware for request logging and monitoring.
Provides structured logging for all API requests.
"""

import time
import logging
from typing import Callable, Awaitable
from fastapi import Request
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
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Record start time
        start_time = time.time()

        # Get request details
        method = request.method
        path = request.url.path
        query_params = str(request.query_params) if request.query_params else ""

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
