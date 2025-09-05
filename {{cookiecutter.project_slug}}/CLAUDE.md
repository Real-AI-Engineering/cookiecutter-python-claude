# CLAUDE.md - {{cookiecutter.project_name}}

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Core Development Principles

IMPORTANT: Follow these principles for ALL code generation:

### Simplicity First
- ALWAYS prefer simple, readable solutions over complex ones
- Use existing patterns in the codebase - don't reinvent wheels
- Avoid over-engineering: if it works in 10 lines, don't write 100
- Every abstraction must justify its existence
- Prefer composition over inheritance
- Write code for humans first, computers second

### Code Quality Standards
- Maximum function length: 20 lines (exceptions require justification)
- Single responsibility principle: one function = one task
- Use descriptive variable names, no single letters except loop counters
- Add comments only for "why", not "what" - code should be self-documenting
- Test coverage minimum: 80% for critical paths

### Decision Making
When solving problems:
1. First, check if there's an existing solution in the codebase
2. Consider the simplest approach that could work
3. Only add complexity when the simple solution fails
4. Document trade-offs in comments

### Common Anti-Patterns to Avoid
- Creating unnecessary abstractions "for future flexibility"
- Complex test logic that's harder to understand than the code
- Reimplementing standard library functionality
- Premature optimization without profiling
- Deep nesting (max 3 levels)

Remember: The best code is code that doesn't need to be written.

## Project Structure

```
{{cookiecutter.project_slug}}/
├── src/
│   └── {{cookiecutter.project_slug}}/     # Main package source code
│       ├── __init__.py
{% if cookiecutter.project_type != "web" -%}
│       ├── cli.py                         # Command-line interface
{% endif -%}
{% if cookiecutter.project_type != "cli" -%}
│       ├── main.py                        # FastAPI application entry point
│       ├── api/                           # API routers and endpoints
│       │   ├── router.py                  # Main API router
│       │   └── health.py                  # Health check endpoints
│       ├── core/                          # Core functionality
│       │   ├── config.py                  # Pydantic v2 settings
│       │   └── logging.py                 # Structured logging setup
│       ├── models/                        # Pydantic data models
│       └── services/                      # Business logic services
{% endif -%}
│       └── py.typed                       # PEP 561 type marker
├── tests/                                 # Test suite
{% if cookiecutter.project_type != "cli" -%}
│   ├── test_health.py                     # Health endpoint tests
│   └── test_main.py                       # Main application tests
{% endif -%}
├── docs/                                  # Documentation
{% if cookiecutter.use_docker == "y" -%}
├── docker/                                # Docker configuration
│   ├── Dockerfile                         # Production image
│   ├── Dockerfile.dev                     # Development image
│   └── docker-compose.yml                 # Local development setup
{% endif -%}
{% if cookiecutter.use_github_actions == "y" -%}
├── .github/workflows/                     # CI/CD workflows
{% endif -%}
├── pyproject.toml                         # Project configuration
├── README.md                              # Project documentation
└── CLAUDE.md                              # This file
```

## Common Commands

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.pypi_package_name}}.git
cd {{cookiecutter.pypi_package_name}}
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

{% if cookiecutter.use_pre_commit == "y" -%}
### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

{% endif -%}
### Testing
```bash
# Run tests with coverage
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_specific.py

# Run tests with coverage report
pytest --cov={{cookiecutter.project_slug}} --cov-report=html
```

### Code Quality
```bash
# Format code
ruff format .

# Lint and fix issues
ruff check . --fix

# Type checking
mypy src/

# Run all quality checks
ruff check . && ruff format --check . && mypy src/
```

### Package Management
```bash
# Install package in development mode
pip install -e .

# Install with optional dependencies
pip install -e ".[dev]"
pip install -e ".[test]"
pip install -e ".[docs]"

# Build package
python -m build

# Install from built package
pip install dist/{{cookiecutter.pypi_package_name}}-{{cookiecutter.first_version}}-py3-none-any.whl
```

{% if cookiecutter.project_type != "web" and cookiecutter.command_line_interface != "None" -%}
### CLI Usage
```bash
# Run CLI tool (after installation)
{{cookiecutter.project_slug}} --help

# Development CLI usage (without installation)
python -m {{cookiecutter.project_slug}}.cli --help
```

{% endif -%}
{% if cookiecutter.project_type != "cli" -%}
### FastAPI Development
```bash
# Start development server with hot reload
uvicorn {{cookiecutter.project_slug}}.main:app --reload

# Start on specific host and port
uvicorn {{cookiecutter.project_slug}}.main:app --host 0.0.0.0 --port 8000 --reload

# Access API documentation
# Open browser: http://localhost:8000/docs (Swagger UI)
# Open browser: http://localhost:8000/redoc (ReDoc)

# Test health endpoints
curl http://localhost:8000/healthz
curl http://localhost:8000/livez
curl http://localhost:8000/readyz
```

{% if cookiecutter.use_docker == "y" -%}
### Docker Development
```bash
# Build production image
docker build -f docker/Dockerfile -t {{cookiecutter.project_slug}}:latest .

# Run production container
docker run -p 8000:8000 {{cookiecutter.project_slug}}:latest

# Development with docker-compose
cd docker && docker-compose up

# Rebuild after changes
cd docker && docker-compose up --build
```

{% endif -%}
{% endif -%}
## Architecture Overview

### Package Structure
- **src/{{cookiecutter.project_slug}}/**: Main package source code following the src layout
{% if cookiecutter.project_type != "web" and cookiecutter.command_line_interface != "None" -%}
- **CLI Interface**: Built with {{cookiecutter.command_line_interface}} for user-friendly command-line interaction
{% endif -%}
{% if cookiecutter.project_type != "cli" -%}
- **FastAPI Application**: Modern async web framework with automatic API documentation
- **API Structure**: Modular router design with versioning support
- **Configuration**: Pydantic v2 Settings for type-safe configuration management
- **Health Checks**: Kubernetes-style health endpoints (healthz, livez, readyz)
{% if cookiecutter.project_type != "cli" -%}
- **Structured Logging**: JSON logging with correlation ID tracking
{% endif -%}
{% endif -%}
- **Testing**: Comprehensive test suite using pytest with coverage reporting
- **Type Safety**: Full type annotations with mypy checking
- **Code Quality**: Automated formatting with ruff and black

### Key Dependencies
{% if cookiecutter.project_type != "web" and cookiecutter.command_line_interface == "Typer" -%}
- **Typer**: Modern CLI framework with automatic help generation
{% elif cookiecutter.project_type != "web" and cookiecutter.command_line_interface == "Click" -%}
- **Click**: Composable command line interface toolkit
{% endif -%}
{% if cookiecutter.project_type != "cli" -%}
- **FastAPI**: High-performance async web framework
- **Pydantic v2**: Data validation and settings management
- **Uvicorn**: ASGI server for production deployment
{% if cookiecutter.project_type != "cli" -%}
- **Structlog**: Structured logging with context preservation
{% endif -%}
{% if cookiecutter.project_type != "cli" -%}
- **asgi-correlation-id**: Request correlation tracking
{% endif -%}
{% endif -%}
- **pytest**: Testing framework with fixtures and plugins
- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checker
- **pyright**: Additional type checking from Microsoft

## Development Patterns

### Code Organization
- Use the `src/` layout for better import handling and testing
- Keep modules focused on single responsibilities  
- Organize related functionality into submodules
- Use `__init__.py` for public API exposure

### Testing Patterns
- Write tests before or alongside implementation (TDD/BDD)
- Use pytest fixtures for test data and setup
- Aim for >80% code coverage on critical paths
- Test both happy path and error conditions
- Mock external dependencies appropriately

### Type Annotations
- Use type hints for all public functions and methods
- Leverage modern Python typing features (Union, Optional, Generic)
- Include `py.typed` marker file for library packages
- Run mypy in CI to catch type errors

### Error Handling
- Use specific exception types rather than generic Exception
- Include helpful error messages with context
- Log errors appropriately with structured logging
- Fail fast and provide clear debugging information

## Key Configuration Files

- **pyproject.toml**: Modern Python project configuration with tool settings
- **pytest.ini** (in pyproject.toml): Test runner configuration with coverage settings
- **ruff configuration**: Linting rules and formatting options
- **mypy configuration**: Type checking strictness and options

## Performance and Optimization Guidelines

- Profile before optimizing - measure twice, cut once
- Use appropriate data structures (sets vs lists, dicts vs sequences)
- Consider memory usage for large data processing
- Cache expensive operations when appropriate
- Use generators for large datasets

## Security Best Practices

- Never commit secrets or API keys to the repository
- Validate and sanitize all external inputs
- Use secure communication protocols (HTTPS, TLS)
- Keep dependencies up to date with security patches
- Follow principle of least privilege for permissions