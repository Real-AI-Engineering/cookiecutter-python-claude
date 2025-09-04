# AGENTS.md - {{cookiecutter.project_name}}

Development workflow guidelines and best practices for AI agents and developers working on this project.

## Project Structure & Module Organization

```
{{cookiecutter.project_slug}}/
├── src/{{cookiecutter.project_slug}}/           # Main package source code
│   ├── __init__.py                              # Package initialization and public API
{% if cookiecutter.command_line_interface != "None" -%}
│   ├── cli.py                                   # Command-line interface
{% endif -%}
│   ├── core/                                    # Core business logic modules
│   ├── utils/                                   # Utility functions and helpers
│   └── py.typed                                 # PEP 561 type marker for mypy
├── tests/                                       # Test suite with pytest
│   ├── __init__.py
│   ├── conftest.py                              # Shared pytest fixtures
│   ├── unit/                                    # Unit tests
│   ├── integration/                             # Integration tests
│   └── fixtures/                                # Test data and fixtures
├── docs/                                        # Documentation
│   ├── api/                                     # API documentation
│   ├── guides/                                  # User guides and tutorials
│   └── development/                             # Development documentation
{% if cookiecutter.use_github_actions == "y" -%}
├── .github/                                     # GitHub-specific configurations
│   ├── workflows/                               # CI/CD workflows
│   │   ├── ci.yml                              # Main CI pipeline
│   │   └── release.yml                         # Release automation
│   ├── ISSUE_TEMPLATE/                         # Issue templates
│   └── pull_request_template.md                # PR template
{% endif -%}
├── scripts/                                     # Development and deployment scripts
├── pyproject.toml                               # Project configuration and dependencies
├── README.md                                    # Project overview and quick start
├── CHANGELOG.md                                 # Version history and changes
├── CONTRIBUTING.md                              # Contribution guidelines
├── CLAUDE.md                                    # Claude Code instructions
└── AGENTS.md                                    # This file
```

## Build, Test, and Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

{% if cookiecutter.use_pre_commit == "y" -%}
### Pre-commit Setup
```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files

# Update hook versions
pre-commit autoupdate
```

{% endif -%}
### Code Quality and Formatting
```bash
# Format code with ruff
ruff format .

# Lint and auto-fix issues
ruff check . --fix

# Type checking with mypy
mypy src/

# Run all quality checks in sequence
ruff check . && ruff format --check . && mypy src/
```

### Testing Commands
```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov={{cookiecutter.project_slug}} --cov-report=html

# Run specific test file or pattern
pytest tests/test_specific.py
pytest -k "test_pattern"

# Run tests with verbose output and stop on first failure
pytest -v -x

# Run tests in parallel (with pytest-xdist)
pytest -n auto
```

### Package Management
```bash
# Install in development mode
pip install -e .

# Build distribution packages
python -m build

# Check package metadata
twine check dist/*

# Upload to PyPI (production)
twine upload dist/*

# Upload to Test PyPI (testing)
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

{% if cookiecutter.command_line_interface != "None" -%}
### CLI Development and Testing
```bash
# Run CLI during development
python -m {{cookiecutter.project_slug}}.cli --help

# Test installed CLI
{{cookiecutter.project_slug}} --version

# Run CLI with specific arguments
{{cookiecutter.project_slug}} [subcommand] [options]
```

{% endif -%}
## Coding Style & Naming Conventions

### Python Style Guidelines
- **Formatting**: Use ruff (line length 88) for consistent code formatting
- **Linting**: Follow ruff rules with strict configuration for code quality
- **Type Hints**: Use type annotations for all public functions and methods
- **Docstrings**: Follow Google or NumPy style docstring conventions
- **Line Length**: Maximum 88 characters (Black/ruff standard)

### Naming Conventions
- **Variables**: `snake_case` for variables and functions
- **Classes**: `PascalCase` for class names  
- **Constants**: `UPPER_CASE` for module-level constants
- **Private**: Prefix with single underscore `_private_method`
- **Files**: `snake_case.py` for Python modules
- **Packages**: `lowercase` or `snake_case` for package names

### Code Organization Patterns
```python
# Module structure template
"""Module docstring describing purpose and usage."""

from __future__ import annotations

import standard_library_imports
import third_party_imports
from your_package import local_imports

# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Type definitions
UserData = dict[str, Any]

class YourClass:
    """Class docstring."""
    
    def __init__(self, param: str) -> None:
        """Initialize with clear parameter documentation."""
        self.param = param
    
    def public_method(self, arg: int) -> str:
        """Public method with type hints and docstring."""
        return self._private_helper(arg)
    
    def _private_helper(self, arg: int) -> str:
        """Private method for internal use."""
        return f"processed_{arg}"

def utility_function(data: UserData) -> bool:
    """Standalone utility function."""
    return bool(data.get("valid", False))
```

## Testing Guidelines

### Testing Framework and Structure
- **Framework**: pytest with plugins (pytest-cov, pytest-mock, pytest-asyncio)
- **Coverage Target**: Minimum 80% line coverage for critical code paths
- **Test Organization**: Separate unit, integration, and end-to-end tests
- **Fixtures**: Use pytest fixtures for test data and setup/teardown

### Testing Best Practices
```python
# Test file naming: test_*.py or *_test.py
# Test class naming: TestClassName
# Test method naming: test_should_do_something_when_condition

import pytest
from unittest.mock import Mock, patch

from {{cookiecutter.project_slug}} import YourClass

class TestYourClass:
    """Test suite for YourClass."""
    
    @pytest.fixture
    def sample_instance(self):
        """Create test instance."""
        return YourClass("test_param")
    
    def test_should_initialize_correctly(self, sample_instance):
        """Test proper initialization."""
        assert sample_instance.param == "test_param"
    
    @patch('{{cookiecutter.project_slug}}.external_dependency')
    def test_should_handle_external_calls(self, mock_external, sample_instance):
        """Test mocking external dependencies."""
        mock_external.return_value = "mocked_result"
        result = sample_instance.method_using_external()
        assert result == "expected_result"
        mock_external.assert_called_once()
    
    def test_should_raise_error_for_invalid_input(self, sample_instance):
        """Test error handling."""
        with pytest.raises(ValueError, match="Invalid input"):
            sample_instance.method_with_validation("invalid")
```

### Testing Checklist
- [ ] Test happy path scenarios
- [ ] Test edge cases and boundary conditions  
- [ ] Test error conditions and exception handling
- [ ] Mock external dependencies appropriately
- [ ] Test async code with pytest-asyncio if applicable
- [ ] Verify test coverage meets minimum requirements
- [ ] Include integration tests for critical workflows

## Commit & Pull Request Guidelines

### Commit Message Format
Follow Conventional Commits specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Commit Types:**
- `feat`: New feature for the user
- `fix`: Bug fix for the user  
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc. (no code change)
- `refactor`: Code refactoring (no functional changes)
- `test`: Adding missing tests or correcting existing tests
- `chore`: Updating build tasks, package manager configs, etc.
- `perf`: Performance improvements
- `ci`: Changes to CI configuration files and scripts

**Examples:**
```
feat(cli): add new export command with JSON format support

fix(parser): handle edge case with empty input files

docs: update installation instructions for Python 3.11

test(utils): add comprehensive tests for string manipulation functions
```

### Pull Request Checklist
Before submitting a pull request, ensure:

- [ ] **Code Quality**: All ruff, black, and mypy checks pass
- [ ] **Tests**: All existing tests pass and new tests cover changes
- [ ] **Coverage**: Maintain or improve test coverage percentage
- [ ] **Documentation**: Update docstrings and README if needed
- [ ] **Changelog**: Update CHANGELOG.md for user-facing changes
- [ ] **Type Hints**: Add type annotations for new functions/methods
- [ ] **Security**: No secrets, API keys, or sensitive data committed
{% if cookiecutter.use_pre_commit == "y" -%}
- [ ] **Pre-commit**: All pre-commit hooks pass successfully
{% endif -%}

### PR Description Template
```markdown
## Summary
Brief description of changes and motivation.

## Changes Made
- Bullet point list of specific changes
- Include any breaking changes

## Testing
- Describe testing approach
- List any new test cases added
- Mention manual testing performed

## Documentation
- List documentation updates made
- Note any additional docs needed

## Checklist
- [ ] Tests pass locally
- [ ] Code follows project style guidelines  
- [ ] Self-review completed
- [ ] Documentation updated if needed
```

## Security & Configuration Guidelines

### Security Best Practices
- **Secrets Management**: Never commit API keys, passwords, or tokens
- **Input Validation**: Validate and sanitize all external inputs
- **Dependencies**: Keep dependencies updated with security patches
- **Permissions**: Follow principle of least privilege
- **Logging**: Avoid logging sensitive information

### Environment Configuration
```bash
# Use environment variables for configuration
export {{cookiecutter.project_slug.upper()}}_API_KEY="your_api_key"
export {{cookiecutter.project_slug.upper()}}_DEBUG="false"
export {{cookiecutter.project_slug.upper()}}_LOG_LEVEL="info"
```

### Dependency Management
- Pin exact versions in production requirements
- Use version ranges in pyproject.toml for compatibility  
- Regularly update dependencies and test for compatibility
- Use tools like `pip-audit` for security vulnerability scanning

```bash
# Check for known vulnerabilities
pip-audit

# Update dependencies
pip install --upgrade -r requirements.txt
```

{% if cookiecutter.use_docker == "y" -%}
## Docker Development

### Local Development with Docker
```bash
# Build development image
docker build -t {{cookiecutter.project_slug}}:dev .

# Run container with volume mount for development
docker run -v $(pwd):/app -it {{cookiecutter.project_slug}}:dev bash

# Run tests in container
docker run --rm {{cookiecutter.project_slug}}:dev pytest

# Run application in container
docker run -p 8000:8000 {{cookiecutter.project_slug}}:dev
```

### Docker Best Practices
- Use multi-stage builds for smaller production images
- Run as non-root user in containers
- Use specific base image versions (not `latest`)
- Minimize layers and optimize for build caching
- Scan images for security vulnerabilities

{% endif -%}
## Continuous Integration & Deployment

{% if cookiecutter.use_github_actions == "y" -%}
### GitHub Actions Workflows
- **CI Pipeline** (`.github/workflows/ci.yml`): 
  - Runs on every push and pull request
  - Tests across multiple Python versions
  - Runs linting, type checking, and security scans
  - Generates and uploads coverage reports

- **Release Pipeline** (`.github/workflows/release.yml`):
  - Triggers on version tags
  - Builds and publishes to PyPI
  - Creates GitHub releases with changelogs

### Branch Protection Rules
Configure branch protection for `main`:
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date
- Restrict pushes to administrators only

{% endif -%}
### Release Process
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with release notes
3. Commit changes: `git commit -m "chore: prepare release v{{cookiecutter.first_version}}"`
4. Create and push tag: `git tag v{{cookiecutter.first_version}} && git push origin v{{cookiecutter.first_version}}`
5. Automated workflow builds and publishes to PyPI
6. Create GitHub release with changelog notes

## Performance and Monitoring

### Performance Guidelines
- Profile code before optimizing (use `cProfile`, `line_profiler`)
- Use appropriate data structures for performance
- Consider memory usage for large datasets
- Implement caching for expensive operations
- Monitor performance regressions in tests

### Logging and Monitoring
```python
import logging
import sys

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('{{cookiecutter.project_slug}}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
```

### Error Tracking
- Use structured logging with appropriate log levels
- Include contextual information in error messages
- Implement proper exception handling with specific exception types
- Consider using error tracking services for production deployments