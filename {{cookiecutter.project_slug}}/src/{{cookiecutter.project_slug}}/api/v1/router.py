{% if cookiecutter.project_type != "cli" -%}
"""API v1 router aggregator."""

from __future__ import annotations

from fastapi import APIRouter

from {{cookiecutter.project_slug}}.api.v1.endpoints import items

router = APIRouter()

# Include all v1 endpoints
router.include_router(items.router, prefix="/items", tags=["items"])

# Add more endpoint routers here as your API grows
# router.include_router(users.router, prefix="/users", tags=["users"])
# router.include_router(auth.router, prefix="/auth", tags=["authentication"])
{% endif -%}