{% if cookiecutter.project_type != "cli" -%}
"""Configuration settings for {{cookiecutter.project_name}}."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings using Pydantic v2."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application settings
    app_name: str = "{{cookiecutter.project_name}}"
    debug: bool = Field(default=False, description="Enable debug mode")
    environment: str = Field(
        default="development", 
        description="Environment (development, staging, production)"
    )

    # Server settings
    host: str = Field(default="0.0.0.0", description="Host to bind the server")
    port: int = Field(default=8000, description="Port to bind the server", ge=1, le=65535)

{% if cookiecutter.project_type != "cli" -%}
    # Logging settings
    log_level: str = Field(
        default="INFO", 
        description="Logging level",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )
    log_format: str = Field(
        default="console" if debug else "json",
        description="Log format (json or console)",
        pattern="^(json|console)$"
    )

{% endif -%}
    # API settings
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 prefix")
    
    # CORS settings
    cors_origins: list[str] = Field(
        default=["*"] if debug else [],
        description="Allowed CORS origins"
    )
    
    # Health check settings
    health_check_grace_period: int = Field(
        default=30,
        description="Grace period for health checks in seconds",
        ge=0
    )


# Global settings instance
settings = Settings()
{% else -%}
"""Configuration placeholder - FastAPI not enabled."""
pass
{% endif -%}