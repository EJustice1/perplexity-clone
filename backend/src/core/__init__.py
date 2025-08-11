"""
Core module for the Perplexity Clone application.
This module provides configuration management and utility functions.
"""

from .config import (
    Config,
    BackendConfig,
    FrontendConfig,
    backend_config,
    frontend_config
)

from .utils import (
    setup_logging,
    timing_decorator,
    safe_get,
    validate_port,
    validate_host,
    format_bytes,
    format_duration,
    ServiceHealth
)

__version__ = "1.0.0"
__author__ = "Perplexity Clone Team"

__all__ = [
    # Configuration
    "Config",
    "BackendConfig",
    "FrontendConfig",
    "backend_config",
    "frontend_config",
    
    # Utilities
    "setup_logging",
    "timing_decorator",
    "safe_get",
    "validate_port",
    "validate_host",
    "format_bytes",
    "format_duration",
    "ServiceHealth"
]
