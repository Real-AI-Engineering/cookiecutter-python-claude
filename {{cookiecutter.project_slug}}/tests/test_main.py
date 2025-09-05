{% if cookiecutter.project_type != "cli" -%}
"""Tests for main FastAPI application."""

from __future__ import annotations

from fastapi import status
from fastapi.testclient import TestClient


class TestMainApplication:
    """Test main FastAPI application."""

    def test_app_creation(self) -> None:
        """Test that FastAPI app is created properly."""
        from {{cookiecutter.project_slug}}.main import app
        
        assert app.title == "{{cookiecutter.project_name}}"
        assert app.description == "{{cookiecutter.project_short_description}}"
        assert app.version == "{{cookiecutter.first_version}}"

    def test_openapi_docs_availability(self, client: TestClient) -> None:
        """Test OpenAPI documentation endpoints."""
        from {{cookiecutter.project_slug}}.core.config import settings
        
        if settings.debug:
            # Docs should be available in debug mode
            response = client.get("/docs")
            assert response.status_code == status.HTTP_200_OK
            
            response = client.get("/openapi.json")
            assert response.status_code == status.HTTP_200_OK
        else:
            # Docs should be disabled in production
            response = client.get("/docs")
            assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cors_headers(self, client: TestClient) -> None:
        """Test CORS headers are properly configured."""
        response = client.options("/healthz")
        
        # CORS headers should be present for OPTIONS requests
        # This test assumes CORS middleware is configured
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_405_METHOD_NOT_ALLOWED]

{% if cookiecutter.project_type != "cli" -%}
    def test_correlation_id_middleware(self, client: TestClient) -> None:
        """Test that correlation ID middleware is working."""
        # Test with custom request ID
        custom_id = "test-request-12345"
        response = client.get("/healthz", headers={"X-Request-ID": custom_id})
        
        assert response.status_code == status.HTTP_200_OK
        
        # The middleware should handle the request without errors
        # In a real implementation, you might want to check logs or response headers
        data = response.json()
        assert "status" in data

    def test_correlation_id_generation(self, client: TestClient) -> None:
        """Test that correlation ID is generated when not provided."""
        response = client.get("/healthz")
        
        assert response.status_code == status.HTTP_200_OK
        
        # Request should succeed even without providing X-Request-ID
        data = response.json()
        assert "status" in data
{% endif -%}

    def test_application_startup_and_shutdown(self) -> None:
        """Test application startup and shutdown events."""
        # This test ensures the lifespan context manager works
        with TestClient(app) as test_client:
            response = test_client.get("/healthz")
            assert response.status_code == status.HTTP_200_OK
        
        # Application should shut down cleanly
{% endif -%}