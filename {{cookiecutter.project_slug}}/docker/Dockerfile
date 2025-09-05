{% if cookiecutter.use_docker == "y" and cookiecutter.project_type != "cli" -%}
# Multi-stage Docker build for {{cookiecutter.project_name}}
# Production-optimized FastAPI application

# Build stage
FROM python:{{cookiecutter.python_version}}-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /build

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY src/ src/

# Build the wheel
RUN pip install --upgrade pip build
RUN python -m build --wheel

# Runtime stage
FROM python:{{cookiecutter.python_version}}-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create app directory and set ownership
WORKDIR /app
RUN chown -R appuser:appuser /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install the wheel
COPY --from=builder /build/dist/*.whl .
RUN pip install --upgrade pip
RUN pip install *.whl
RUN rm *.whl

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "{{cookiecutter.project_slug}}.main:app", "--host", "0.0.0.0", "--port", "8000"]
{% elif cookiecutter.use_docker == "y" -%}
# Basic Docker build for {{cookiecutter.project_name}}
# CLI application

FROM python:{{cookiecutter.python_version}}-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create app directory
WORKDIR /app
RUN chown -R appuser:appuser /app

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY src/ src/

# Install the package
RUN pip install --upgrade pip
RUN pip install -e .

# Switch to non-root user
USER appuser

# Default command
CMD ["python", "-m", "{{cookiecutter.project_slug}}"]
{% endif -%}