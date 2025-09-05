"""Shared pytest fixtures for {{cookiecutter.project_name}} tests."""

from __future__ import annotations

import pytest
{% if cookiecutter.project_type != "cli" -%}
from fastapi.testclient import TestClient

from {{cookiecutter.project_slug}}.main import app


@pytest.fixture
def client() -> TestClient:
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_data() -> dict[str, str]:
    """Sample data for testing."""
    return {"test": "data", "foo": "bar"}
{% else -%}


@pytest.fixture
def sample_data() -> dict[str, str]:
    """Sample data for testing."""
    return {"test": "data", "foo": "bar"}
{% endif -%}