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
{% if cookiecutter.command_line_interface != "None" -%}
│       ├── cli.py                         # Command-line interface
{% endif -%}
│       └── py.typed                       # PEP 561 type marker
├── tests/                                 # Test suite
├── docs/                                  # Documentation
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

{% if cookiecutter.command_line_interface != "None" -%}
### CLI Usage
```bash
# Run CLI tool (after installation)
{{cookiecutter.project_slug}} --help

# Development CLI usage (without installation)
python -m {{cookiecutter.project_slug}}.cli --help
```

{% endif -%}
## Architecture Overview

### Package Structure
- **src/{{cookiecutter.project_slug}}/**: Main package source code following the src layout
{% if cookiecutter.command_line_interface != "None" -%}
- **CLI Interface**: Built with {{cookiecutter.command_line_interface}} for user-friendly command-line interaction
{% endif -%}
- **Testing**: Comprehensive test suite using pytest with coverage reporting
- **Type Safety**: Full type annotations with mypy checking
- **Code Quality**: Automated formatting with ruff and black

### Key Dependencies
{% if cookiecutter.command_line_interface == "Typer" -%}
- **Typer**: Modern CLI framework with automatic help generation
{% elif cookiecutter.command_line_interface == "Click" -%}
- **Click**: Composable command line interface toolkit
{% endif -%}
- **pytest**: Testing framework with fixtures and plugins
- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checker

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