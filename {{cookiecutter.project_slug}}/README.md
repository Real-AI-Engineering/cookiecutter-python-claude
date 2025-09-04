# {{cookiecutter.project_name}}

{{cookiecutter.project_short_description}}

[![Python](https://img.shields.io/badge/python-{{cookiecutter.python_version}}+-blue.svg)](https://www.python.org/downloads/)
{% if cookiecutter.license != "Proprietary" -%}
[![License: {{cookiecutter.license}}](https://img.shields.io/badge/License-{{cookiecutter.license}}-yellow.svg)](LICENSE)
{% endif -%}
{% if cookiecutter.use_github_actions == "y" -%}
[![CI](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.pypi_package_name}}/workflows/CI/badge.svg)](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.pypi_package_name}}/actions)
[![Coverage](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.pypi_package_name}}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{cookiecutter.github_username}}/{{cookiecutter.pypi_package_name}})
{% endif -%}
[![PyPI version](https://badge.fury.io/py/{{cookiecutter.pypi_package_name}}.svg)](https://badge.fury.io/py/{{cookiecutter.pypi_package_name}})
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Features

- 🐍 **Modern Python**: Built for Python {{cookiecutter.python_version}}+ with full type annotations
- 🧪 **Testing Ready**: Comprehensive test suite with pytest and coverage reporting
- 🔧 **Developer Friendly**: Pre-configured with ruff, mypy, and modern Python tooling
{% if cookiecutter.command_line_interface != "None" -%}
- ⚡ **CLI Interface**: Command-line tool built with {{cookiecutter.command_line_interface}}
{% endif -%}
{% if cookiecutter.use_github_actions == "y" -%}
- 🚀 **CI/CD Ready**: GitHub Actions workflow for automated testing and deployment
{% endif -%}
{% if cookiecutter.use_pre_commit == "y" -%}
- 🪝 **Pre-commit Hooks**: Automated code quality checks before commits
{% endif -%}
- 📦 **Modern Packaging**: Uses `pyproject.toml` and follows latest packaging standards

## Installation

### From PyPI

```bash
pip install {{cookiecutter.pypi_package_name}}
```

### From Source

```bash
git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.pypi_package_name}}.git
cd {{cookiecutter.pypi_package_name}}
pip install -e ".[dev]"
```

## Quick Start

### Python API

```python
import {{cookiecutter.project_slug}}

# Use your package here
print(f"{{cookiecutter.project_name}} v{{ '{'}}{{cookiecutter.project_slug}}.__version__{{ '}' }}")
```

{% if cookiecutter.command_line_interface != "None" -%}
### Command Line Interface

```bash
# Show help
{{cookiecutter.project_slug}} --help

# Show version
{{cookiecutter.project_slug}} --version

# Example command
{{cookiecutter.project_slug}} hello --count 3
```
{% endif %}

## Development

### Setup Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.pypi_package_name}}.git
   cd {{cookiecutter.pypi_package_name}}
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

{% if cookiecutter.use_pre_commit == "y" -%}
4. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```
{% endif %}

### Development Commands

#### Code Quality
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

#### Testing
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov={{cookiecutter.project_slug}}

# Run tests with HTML coverage report
pytest --cov={{cookiecutter.project_slug}} --cov-report=html
```

#### Building and Distribution
```bash
# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI (after building)
twine upload dist/*
```

### Project Structure

```
{{cookiecutter.pypi_package_name}}/
├── src/{{cookiecutter.project_slug}}/         # Main package source code
│   ├── __init__.py                           # Package initialization
{% if cookiecutter.command_line_interface != "None" -%}
│   ├── cli.py                                # Command-line interface  
{% endif -%}
│   └── py.typed                              # PEP 561 type marker
├── tests/                                    # Test suite
├── docs/                                     # Documentation
{% if cookiecutter.use_github_actions == "y" -%}
├── .github/workflows/                        # GitHub Actions CI/CD
{% endif -%}
├── pyproject.toml                            # Project configuration
├── README.md                                 # This file
├── CLAUDE.md                                 # Claude Code instructions
├── AGENTS.md                                 # Development guidelines
{% if cookiecutter.license != "Proprietary" -%}
├── LICENSE                                   # License file
{% endif -%}
└── .gitignore                                # Git ignore rules
```

## Contributing

We welcome contributions! Please see our [contributing guidelines](AGENTS.md) for details on:

- Setting up the development environment
- Running tests and quality checks
- Submitting pull requests
- Code style and conventions

### Development Guidelines

- **Code Style**: We use `ruff` for formatting and linting
- **Type Hints**: All public APIs should have complete type annotations
- **Testing**: Maintain test coverage above 80% for critical code paths
- **Documentation**: Update documentation for any user-facing changes
- **Commits**: Follow [Conventional Commits](https://www.conventionalcommits.org/) format

### Quick Contribution Checklist

- [ ] Code passes all tests (`pytest`)
- [ ] Code passes linting (`ruff check .`)
- [ ] Code is properly formatted (`ruff format .`)
- [ ] Type checking passes (`mypy src/`)
- [ ] Documentation is updated if needed
- [ ] Tests added for new functionality

## Documentation

- **[CLAUDE.md](CLAUDE.md)**: Instructions for Claude Code integration
- **[AGENTS.md](AGENTS.md)**: Development workflow and guidelines
{% if cookiecutter.use_github_actions == "y" -%}
- **[GitHub Actions](.github/workflows/)**: CI/CD pipeline configuration
{% endif -%}

## Requirements

- Python {{cookiecutter.python_version}}+
{% if cookiecutter.command_line_interface == "Typer" -%}
- Typer (for CLI functionality)
{% elif cookiecutter.command_line_interface == "Click" -%}
- Click (for CLI functionality)
{% endif -%}

## License

{% if cookiecutter.license == "MIT" -%}
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
{% elif cookiecutter.license == "BSD-3-Clause" -%}
This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.
{% elif cookiecutter.license == "Apache-2.0" -%}
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
{% elif cookiecutter.license == "GPL-3.0" -%}
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
{% elif cookiecutter.license == "Proprietary" -%}
This project is proprietary software. All rights reserved.
{% endif %}

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

## Support

- 📫 **Issues**: [GitHub Issues](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.pypi_package_name}}/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.pypi_package_name}}/discussions)
- 📧 **Email**: {{cookiecutter.email}}

## Acknowledgments

- Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [cookiecutter-python-claude](https://github.com/username/cookiecutter-python-claude) template
- Follows modern Python packaging standards and best practices