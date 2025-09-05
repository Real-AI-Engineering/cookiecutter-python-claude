{% if cookiecutter.project_type != "cli" -%}
"""Kubernetes-style health check endpoints for {{cookiecutter.project_name}}."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, status
from pydantic import BaseModel

from {{cookiecutter.project_slug}}.core.config import settings
{% if cookiecutter.project_type != "cli" -%}
from {{cookiecutter.project_slug}}.core.logging import logger
{% else -%}
import logging

logger = logging.getLogger(__name__)
{% endif -%}

# Store application start time for uptime calculation
_start_time = time.time()

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str
    timestamp: datetime
    uptime_seconds: float
    version: str = "{{cookiecutter.first_version}}"


class ReadinessResponse(BaseModel):
    """Readiness check response model."""
    
    status: str
    timestamp: datetime
    checks: dict[str, Any]


@router.get(
    "/healthz",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    description="Returns application health status (Kubernetes liveness probe)",
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint for Kubernetes liveness probe.
    
    This endpoint indicates whether the application is running and responsive.
    If this endpoint fails, Kubernetes will restart the pod.
    """
    uptime = time.time() - _start_time
    
    response = HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        uptime_seconds=round(uptime, 2),
    )
    
    logger.info("Health check requested", uptime_seconds=uptime)
    return response


@router.get(
    "/livez", 
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness check endpoint",
    description="Indicates if the application is alive and running",
)
async def liveness_check() -> HealthResponse:
    """
    Liveness probe endpoint for Kubernetes.
    
    This endpoint checks if the application process is running.
    Similar to healthz but can include additional liveness-specific checks.
    """
    uptime = time.time() - _start_time
    
    response = HealthResponse(
        status="alive", 
        timestamp=datetime.now(timezone.utc),
        uptime_seconds=round(uptime, 2),
    )
    
    logger.debug("Liveness check requested")
    return response


@router.get(
    "/readyz",
    response_model=ReadinessResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness check endpoint", 
    description="Indicates if the application is ready to serve traffic",
)
async def readiness_check() -> ReadinessResponse:
    """
    Readiness probe endpoint for Kubernetes.
    
    This endpoint checks if the application is ready to handle requests.
    It should verify that all dependencies (database, external services, etc.)
    are available and the application can serve traffic.
    
    If this endpoint fails, Kubernetes will stop sending traffic to this pod
    but won't restart it.
    """
    checks: dict[str, Any] = {}
    
    # Add dependency checks here
    # For example:
    # checks["database"] = await check_database_connection()
    # checks["redis"] = await check_redis_connection()
    # checks["external_api"] = await check_external_api()
    
    # Basic readiness checks
    checks["startup_complete"] = True
    checks["configuration_loaded"] = settings.app_name is not None
    
    # Check if we're past the startup grace period
    uptime = time.time() - _start_time
    checks["startup_grace_period"] = uptime > settings.health_check_grace_period
    
    # Determine overall status
    all_checks_passed = all(
        check_result is True 
        for check_result in checks.values() 
        if isinstance(check_result, bool)
    )
    
    response_status = "ready" if all_checks_passed else "not_ready"
    
    response = ReadinessResponse(
        status=response_status,
        timestamp=datetime.now(timezone.utc),
        checks=checks,
    )
    
    logger.info("Readiness check requested", status=response_status, checks=checks)
    
    # Return 503 Service Unavailable if not ready
    if not all_checks_passed:
        router.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    
    return response


# Legacy endpoint for backward compatibility
@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Legacy health endpoint",
    description="Legacy health check endpoint (use /healthz instead)",
    deprecated=True,
)
async def legacy_health_check() -> HealthResponse:
    """Legacy health check endpoint for backward compatibility."""
    logger.warning("Legacy health endpoint used, prefer /healthz")
    return await health_check()
{% endif -%}