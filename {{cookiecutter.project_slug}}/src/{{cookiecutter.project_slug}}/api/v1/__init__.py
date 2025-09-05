{% if cookiecutter.project_type != "cli" -%}
"""API v1 package."""

from {{cookiecutter.project_slug}}.api.v1.router import router as v1_router

__all__ = ["v1_router"]
{% endif -%}