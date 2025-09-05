{% if cookiecutter.project_type != "cli" -%}
"""FastAPI application entry point for {{cookiecutter.project_name}}."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
{% if cookiecutter.project_type != "cli" -%}
from asgi_correlation_id import CorrelationIdMiddleware
{% endif -%}

{% if cookiecutter.project_type != "cli" -%}
from {{cookiecutter.project_slug}}.core.logging import setup_logging
{% endif -%}
from {{cookiecutter.project_slug}}.core.config import settings
from {{cookiecutter.project_slug}}.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
{% if cookiecutter.project_type != "cli" %}    setup_logging(debug=settings.debug, log_format=settings.log_format)
{% endif %}    logging.info("{{cookiecutter.project_name}} starting up...")
    yield
    # Shutdown
    logging.info("{{cookiecutter.project_name}} shutting down...")


app = FastAPI(
    title=settings.app_name,
    description="{{cookiecutter.project_short_description}}",
    version="{{cookiecutter.first_version}}",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

{% if cookiecutter.project_type != "cli" -%}
# Add correlation ID middleware for request tracing
app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Request-ID",
    generator=lambda: __import__("uuid").uuid4().hex,
)

{% endif -%}
# Include API router
app.include_router(api_router)


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint redirect to docs."""
    return {"message": "{{cookiecutter.project_name}} API", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "{{cookiecutter.project_slug}}.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
{% endif -%}