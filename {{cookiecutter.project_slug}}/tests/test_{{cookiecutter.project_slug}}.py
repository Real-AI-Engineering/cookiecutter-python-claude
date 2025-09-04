"""Tests for {{cookiecutter.project_name}}."""

from __future__ import annotations

import {{cookiecutter.project_slug}}


def test_version():
    """Test that version is defined."""
    assert hasattr({{cookiecutter.project_slug}}, "__version__")
    assert isinstance({{cookiecutter.project_slug}}.__version__, str)
    assert len({{cookiecutter.project_slug}}.__version__) > 0


def test_author():
    """Test that author is defined."""
    assert hasattr({{cookiecutter.project_slug}}, "__author__")
    assert {{cookiecutter.project_slug}}.__author__ == "{{cookiecutter.full_name}}"


def test_email():
    """Test that email is defined."""
    assert hasattr({{cookiecutter.project_slug}}, "__email__")
    assert {{cookiecutter.project_slug}}.__email__ == "{{cookiecutter.email}}"


def test_import():
    """Test that the module can be imported."""
    import {{cookiecutter.project_slug}}
    
    # Basic smoke test
    assert {{cookiecutter.project_slug}} is not None


def test_sample_fixture(sample_data):
    """Test using a pytest fixture."""
    assert "test" in sample_data
    assert sample_data["test"] == "data"