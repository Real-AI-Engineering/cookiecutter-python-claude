# Cookiecutter Python Claude Template

A modern, feature-rich [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for Python projects with comprehensive Claude Code integration and development best practices.

## Features

### 🐍 Modern Python Setup
- **Python 3.10+ Support**: Choose your minimum Python version
- **Source Layout**: Uses `src/` layout for better import handling
- **Type Safety**: Full type annotations with mypy checking
- **Modern Packaging**: Uses `pyproject.toml` instead of `setup.py`

### 🤖 Claude Code Integration
- **CLAUDE.md**: Comprehensive instructions for Claude Code with your development principles
- **AGENTS.md**: Detailed workflow guidelines for AI agents and developers
- **Best Practices**: Embedded simplicity-first development principles
- **Project-Specific Instructions**: Tailored guidance for each generated project

### 🔧 Developer Experience
- **Multiple CLI Options**: Choose from Typer, Click, argparse, or none
- **Pre-commit Hooks**: Optional automated code quality checks
- **Modern Tooling**: ruff (linting/formatting), mypy (type checking), pytest (testing)
- **GitHub Actions**: Optional CI/CD pipeline with multi-OS testing
- **Docker Support**: Optional Docker configuration

### 📦 Production Ready
- **Comprehensive Testing**: pytest setup with coverage reporting
- **Security Scanning**: Bandit and safety checks in CI
- **Package Building**: Automated wheel building and PyPI publishing
- **Documentation**: README templates with badges and comprehensive guides

## Quick Start

### Prerequisites
```bash
pip install cookiecutter
```

### Generate a Project
```bash
# From GitHub (recommended)
cookiecutter gh:yourusername/cookiecutter-python-claude

# From local directory
cookiecutter /path/to/cookiecutter-python-claude
```

### Interactive Setup
The template will prompt you for:

```
full_name [Your Name]: John Doe
email [your.email@example.com]: john@example.com
github_username [yourusername]: johndoe
project_name [My Python Project]: Awesome Python Tool
project_slug [awesome_python_tool]: 
pypi_package_name [awesome-python-tool]:
project_short_description [A Python project created with best practices]: A tool for awesome Python development
first_version [0.1.0]: 
python_version [3.10]: 3.11
command_line_interface [None]: Typer
use_github_actions [y]: y
use_pre_commit [y]: y
license [MIT]: MIT
create_author_file [y]: n
use_docker [y]: n
```

## Generated Project Structure

```
awesome-python-tool/
├── src/awesome_python_tool/
│   ├── __init__.py              # Package initialization
│   ├── cli.py                   # Optional CLI (Typer/Click/argparse)
│   └── py.typed                 # PEP 561 type marker
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_awesome_python_tool.py
│   └── test_cli.py              # CLI tests (if enabled)
├── .github/workflows/
│   └── ci.yml                   # GitHub Actions CI/CD
├── docs/                        # Documentation directory
├── scripts/                     # Development scripts
├── pyproject.toml               # Modern Python configuration
├── README.md                    # Project documentation
├── CLAUDE.md                    # Claude Code instructions
├── AGENTS.md                    # Development guidelines
├── LICENSE                      # License file
├── .gitignore                   # Git ignore rules
└── .pre-commit-config.yaml      # Pre-commit hooks (if enabled)
```

## Template Configuration Options

### Basic Information
- **full_name**: Your full name (for package metadata)
- **email**: Your email address
- **github_username**: Your GitHub username
- **project_name**: Human-readable project name
- **project_slug**: Python package name (auto-generated from project_name)
- **pypi_package_name**: PyPI package name (auto-generated)
- **project_short_description**: Brief project description

### Technical Configuration
- **python_version**: Minimum Python version (3.10, 3.11, 3.12, 3.13)
- **command_line_interface**: CLI framework (None, Typer, Click, argparse)
- **use_github_actions**: Set up GitHub Actions CI/CD (y/n)
- **use_pre_commit**: Set up pre-commit hooks (y/n)
- **license**: License type (MIT, BSD-3-Clause, Apache-2.0, GPL-3.0, Proprietary)
- **create_author_file**: Create AUTHORS.md file (y/n)
- **use_docker**: Include Docker configuration (y/n)

## Key Features Explained

### CLAUDE.md Integration
Every generated project includes a comprehensive `CLAUDE.md` file with:
- **Core Development Principles**: Simplicity-first approach, code quality standards
- **Project Structure**: Clear overview of the codebase organization
- **Common Commands**: Development, testing, and deployment commands
- **Architecture Overview**: Key patterns and dependencies
- **Best Practices**: Error handling, performance, security guidelines

### AGENTS.md Workflow Guidelines
The `AGENTS.md` file provides detailed guidelines for:
- **Project Structure**: Module organization and conventions
- **Development Commands**: Setup, testing, quality checks
- **Coding Standards**: Python style, naming conventions, code organization
- **Testing Practices**: Framework setup, coverage requirements, testing patterns
- **CI/CD Workflows**: Commit conventions, PR guidelines, release processes

### Modern Python Tooling

#### Code Quality
- **ruff**: Fast Python linter and formatter (replaces flake8, isort, black)
- **mypy**: Static type checker with strict configuration
- **bandit**: Security vulnerability scanner
- **safety**: Dependency vulnerability checker

#### Testing
- **pytest**: Modern testing framework with plugins
- **pytest-cov**: Coverage reporting with HTML output
- **pytest-mock**: Mocking utilities for tests

#### CI/CD Pipeline
The GitHub Actions workflow includes:
- Multi-OS testing (Ubuntu, Windows, macOS)
- Multi-Python version testing
- Code quality checks (linting, formatting, type checking)
- Security scanning
- Test coverage reporting
- Package building and validation
- Optional integration testing

## Development Commands

After generating a project, you can immediately start developing:

```bash
cd your-project-name

# Set up development environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"

# Install pre-commit hooks (if enabled)
pre-commit install

# Run tests
pytest

# Check code quality
ruff check . --fix
ruff format .
mypy src/

# Build package
python -m build
```

## Customization

### Hooks System
The template includes Python hooks for validation and cleanup:

- **pre_gen_project.py**: Validates user inputs (project names, email format, etc.)
- **post_gen_project.py**: Cleans up unused files and initializes git repository

### Adding New Features
To customize the template:

1. **Modify cookiecutter.json**: Add new configuration options
2. **Update templates**: Use Jinja2 templating in any file
3. **Extend hooks**: Add validation or cleanup logic
4. **Test locally**: Generate projects and test the output

### Example Customization
```json
{
  "use_fastapi": ["y", "n"],
  "database_type": ["sqlite", "postgresql", "mysql", "none"]
}
```

Then in your templates:
```python
{% if cookiecutter.use_fastapi == "y" -%}
dependencies = ["fastapi", "uvicorn"]
{% endif %}
```

## Best Practices Embedded

### Simplicity First
- Prefer simple, readable solutions over complex ones
- Use existing patterns - don't reinvent wheels
- Avoid over-engineering
- Maximum function length: 20 lines
- Single responsibility principle

### Code Quality Standards
- Full type annotations
- Comprehensive test coverage (>80%)
- Descriptive variable names
- Comments for "why", not "what"
- Automated formatting and linting

### Security Considerations
- Never commit secrets
- Input validation
- Dependency vulnerability scanning
- Secure defaults in configuration

## Contributing

We welcome contributions to improve this template! Please:

1. **Fork the repository**
2. **Create a feature branch**
3. **Test your changes** by generating projects
4. **Submit a pull request**

### Testing the Template
```bash
# Generate a test project
cookiecutter . --no-input

# Test the generated project
cd python-boilerplate
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Requirements

- **Python 3.8+** (for running cookiecutter)
- **cookiecutter** (`pip install cookiecutter`)
- **Git** (for repository initialization)

Generated projects require:
- **Python 3.10+** (configurable)
- Modern Python packaging tools (pip, build)

## License

This template is licensed under the MIT License. Generated projects use the license you select during generation.

## Acknowledgments

- Inspired by modern Python packaging standards
- Built for seamless Claude Code integration  
- Follows [Python Packaging Authority](https://www.pypa.io/) recommendations
- Uses best practices from the Python community

## Changelog

### v1.0.0
- Initial release with full Claude Code integration
- Modern Python tooling (ruff, mypy, pytest)
- Multi-CLI framework support
- Comprehensive CI/CD pipeline
- Security scanning integration
- Docker support

## Support

- 📫 **Issues**: [GitHub Issues](https://github.com/yourusername/cookiecutter-python-claude/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/cookiecutter-python-claude/discussions)

---

**Happy coding with modern Python and Claude Code! 🚀**