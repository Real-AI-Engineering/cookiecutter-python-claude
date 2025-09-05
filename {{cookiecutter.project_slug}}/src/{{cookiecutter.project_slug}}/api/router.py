{% if cookiecutter.project_type != "cli" -%}
"""Main API router for {{cookiecutter.project_name}}."""

from __future__ import annotations

from fastapi import APIRouter

from {{cookiecutter.project_slug}}.api import health
from {{cookiecutter.project_slug}}.api.v1 import v1_router
from {{cookiecutter.project_slug}}.core.config import settings

# Create main API router
api_router = APIRouter()

# Include health endpoints
api_router.include_router(health.router, tags=["health"])

# Include versioned API routers
api_router.include_router(
    v1_router, 
    prefix=settings.api_v1_prefix,
    tags=["v1"]
)
{% endif -%}