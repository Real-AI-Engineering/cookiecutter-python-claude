---
allowed-tools: Bash, Read, Write, Task
---

# Python-Specific PM Commands

Additional project management commands tailored for Python development with uv, pytest, ruff, and mypy.

## /pm:deps-check

Check and validate Python dependencies:

```bash
# Check for outdated packages
uv pip list --outdated

# Check for security vulnerabilities
uv pip audit || pip-audit

# Verify all dependencies installed
uv pip check

# Show dependency tree
uv pip show --tree {{cookiecutter.project_slug}}
```

Output format:
```
📦 Dependency Status
===================
✅ All dependencies installed
⚠️ 3 packages outdated
❌ 1 security vulnerability found

Outdated:
- pytest: 7.3.0 -> 7.4.0
- ruff: 0.1.0 -> 0.2.0
- mypy: 1.5.0 -> 1.6.0

Vulnerabilities:
- package-name: CVE-2024-XXXX (High)

Run: uv pip install --upgrade [packages]
```

## /pm:lint-fix

Run automated code quality fixes:

```bash
# Fix linting issues
ruff check . --fix

# Format code
ruff format .

# Sort imports
ruff check . --select I --fix

# Check for remaining issues
ruff check .
```

Report format:
```
🔧 Code Quality Fixes
====================
✅ Fixed 12 linting issues
✅ Formatted 8 files
✅ Sorted imports in 5 files

Remaining issues (manual fix required):
- src/module.py:45: Possible undefined name
- tests/test_app.py:12: Unused import
```

## /pm:type-check

Run type checking with detailed analysis:

```bash
# Run mypy with strict settings
mypy src/ --strict

# Generate HTML report
mypy src/ --html-report mypy-report

# Check specific file
mypy src/{{cookiecutter.project_slug}}/main.py

# Ignore missing imports
mypy src/ --ignore-missing-imports
```

Analysis format:
```
🔍 Type Check Results
====================
Files checked: 25
Errors: 3
Warnings: 7

Errors:
1. src/api/routes.py:34
   Incompatible return type: expected str, got int

2. src/models/user.py:12
   Missing type annotation for 'process_data'

3. src/utils/helpers.py:56
   Argument 1 has incompatible type

Fix suggestions provided in comments.
```

## /pm:coverage-report

Generate and analyze test coverage:

```bash
# Run tests with coverage
uv run pytest --cov={{cookiecutter.project_slug}} --cov-report=term-missing --cov-report=html

# Check coverage threshold
coverage report --fail-under=80

# Find uncovered lines
coverage report --skip-covered --show-missing

# Generate badge
coverage-badge -o coverage.svg
```

Report format:
```
📊 Coverage Report
==================
Overall: 87.3% ✅

Module Coverage:
- api/: 92.1% ✅
- models/: 88.5% ✅
- utils/: 76.2% ⚠️
- services/: 83.9% ✅

Uncovered Critical Paths:
- src/api/auth.py: lines 45-52 (error handling)
- src/models/validation.py: lines 23-28 (edge case)

HTML Report: htmlcov/index.html
```

## /pm:security-scan

Run security checks on code and dependencies:

```bash
# Check for security issues in code
bandit -r src/ -f json

# Check dependencies
pip-audit

# Check for hardcoded secrets
detect-secrets scan

# SAST analysis
semgrep --config=auto src/
```

## /pm:docs-build

Build and validate documentation:

```bash
# Build Sphinx docs
cd docs && make html

# Check docstring coverage
pydocstyle src/

# Generate API docs
sphinx-apidoc -o docs/api src/

# Validate README
python -m readme_renderer README.md
```

## /pm:perf-profile

Profile code performance:

```bash
# Run with profiling
python -m cProfile -o profile.stats src/{{cookiecutter.project_slug}}/main.py

# Analyze profile
python -m pstats profile.stats

# Memory profiling
python -m memory_profiler src/{{cookiecutter.project_slug}}/main.py

# Line profiling
kernprof -l -v src/{{cookiecutter.project_slug}}/main.py
```

## /pm:pre-commit

Run pre-commit checks:

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks
pre-commit run --all-files

# Update hooks
pre-commit autoupdate

# Run specific hook
pre-commit run ruff --all-files
```

## /pm:package-build

Build Python package for distribution:

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build wheel and sdist
python -m build

# Check package
twine check dist/*

# Test installation
pip install dist/*.whl

# Upload to TestPyPI
twine upload --repository testpypi dist/*
```

## /pm:env-setup

Setup development environment:

```bash
# Create virtual environment with uv
uv venv

# Activate environment
source .venv/bin/activate

# Install package in editable mode
uv pip install -e ".[dev,test,docs]"

# Install pre-commit hooks
pre-commit install

# Verify setup
python -c "import {{cookiecutter.project_slug}}; print({{cookiecutter.project_slug}}.__version__)"
```

## Integration with Standard PM Commands

These Python commands integrate with standard PM workflow:

1. **During PRD Development:**
   - Run `/pm:deps-check` to verify technical feasibility
   - Use `/pm:security-scan` for security requirements

2. **During Implementation:**
   - Run `/pm:lint-fix` before each commit
   - Use `/pm:type-check` to maintain type safety
   - Execute `/pm:coverage-report` to ensure test coverage

3. **Before Sync to GitHub:**
   - Run `/pm:pre-commit` for final checks
   - Use `/pm:docs-build` to update documentation
   - Execute `/pm:package-build` if releasing

4. **In CI/CD Pipeline:**
   - All these commands can be used in GitHub Actions
   - Integrate with `/pm:issue-sync` for status updates

## Command Aliases

For convenience, these shorter aliases are available:

- `/pm:deps` → `/pm:deps-check`
- `/pm:lint` → `/pm:lint-fix`
- `/pm:type` → `/pm:type-check`
- `/pm:cov` → `/pm:coverage-report`
- `/pm:sec` → `/pm:security-scan`
- `/pm:docs` → `/pm:docs-build`
- `/pm:perf` → `/pm:perf-profile`
- `/pm:pre` → `/pm:pre-commit`
- `/pm:build` → `/pm:package-build`
- `/pm:env` → `/pm:env-setup`

$ARGUMENTS