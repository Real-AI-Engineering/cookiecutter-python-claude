"""Shared pytest fixtures for {{cookiecutter.project_name}} tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def sample_data() -> dict[str, str]:
    """Sample data for testing."""
    return {"test": "data", "foo": "bar"}