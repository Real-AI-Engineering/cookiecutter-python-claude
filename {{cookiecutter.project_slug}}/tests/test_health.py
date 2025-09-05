{% if cookiecutter.project_type != "cli" -%}
"""Tests for health check endpoints."""

from __future__ import annotations

import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_healthz_endpoint(self, client: TestClient) -> None:
        """Test /healthz endpoint returns healthy status."""
        response = client.get("/healthz")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "uptime_seconds" in data
        assert isinstance(data["uptime_seconds"], (int, float))
        assert data["uptime_seconds"] >= 0
        assert data["version"] == "{{cookiecutter.first_version}}"

    def test_livez_endpoint(self, client: TestClient) -> None:
        """Test /livez endpoint returns alive status."""
        response = client.get("/livez")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["status"] == "alive"
        assert "timestamp" in data
        assert "uptime_seconds" in data
        assert isinstance(data["uptime_seconds"], (int, float))

    def test_readyz_endpoint(self, client: TestClient) -> None:
        """Test /readyz endpoint returns readiness status."""
        response = client.get("/readyz")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["status"] in ["ready", "not_ready"]
        assert "timestamp" in data
        assert "checks" in data
        assert isinstance(data["checks"], dict)
        
        # Check expected readiness checks
        checks = data["checks"]
        assert "startup_complete" in checks
        assert "configuration_loaded" in checks
        assert "startup_grace_period" in checks

    def test_legacy_health_endpoint(self, client: TestClient) -> None:
        """Test legacy /health endpoint works but is deprecated."""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "uptime_seconds" in data

    def test_root_endpoint(self, client: TestClient) -> None:
        """Test root endpoint returns basic info."""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert data["docs"] == "/docs"

    @pytest.mark.asyncio
    async def test_health_endpoints_response_time(self, client: TestClient) -> None:
        """Test that health endpoints respond quickly."""
        import time
        
        endpoints = ["/healthz", "/livez", "/readyz"]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            assert response.status_code == status.HTTP_200_OK
            
            # Health checks should be fast (< 1 second)
            response_time = end_time - start_time
            assert response_time < 1.0, f"{endpoint} took {response_time:.2f}s to respond"

    def test_health_endpoints_multiple_calls(self, client: TestClient) -> None:
        """Test health endpoints handle multiple concurrent calls."""
        endpoints = ["/healthz", "/livez", "/readyz"]
        
        for endpoint in endpoints:
            # Make multiple calls to ensure consistency
            responses = [client.get(endpoint) for _ in range(5)]
            
            for response in responses:
                assert response.status_code == status.HTTP_200_OK
                data = response.json()
                assert "timestamp" in data
{% endif -%}