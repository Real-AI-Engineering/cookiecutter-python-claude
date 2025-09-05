{% if cookiecutter.project_type != "cli" -%}
"""Structured logging configuration for {{cookiecutter.project_name}}."""

from __future__ import annotations

import logging
import sys
from typing import Any

import structlog
{% if cookiecutter.project_type != "cli" -%}
from asgi_correlation_id.context import correlation_id
{% endif -%}


def add_correlation_id(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    """Add correlation ID to log records."""
{% if cookiecutter.project_type != "cli" -%}
    if request_id := correlation_id.get(None):
        event_dict["request_id"] = request_id
{% endif -%}
    return event_dict


def setup_logging(debug: bool = False, log_format: str = "console") -> None:
    """Configure structured logging with structlog."""
    
    # Configure structlog
    processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        add_correlation_id,
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
    ]
    
    if debug or log_format == "console":
        # Console-friendly output for development
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
    else:
        # JSON output for production
        processors.append(structlog.processors.JSONRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        context_class=dict,
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("uvicorn").setLevel(logging.WARNING if not debug else logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING if not debug else logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.WARNING if not debug else logging.INFO)


# Create a logger instance
logger = structlog.get_logger(__name__)
{% else -%}
"""Logging placeholder - structlog not enabled."""

import logging

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
{% endif -%}