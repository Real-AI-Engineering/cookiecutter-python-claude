---
allowed-tools: Bash, Read, Write, LS
---

# Prime Python Testing Environment

This command prepares the Python testing environment with pytest, coverage tools, and configures the pytest-runner agent for optimal test execution.

## Preflight Checklist

Complete these validation steps before proceeding.

### 1. Python Environment Detection

Check Python version and package manager:
```bash
python --version 2>/dev/null || python3 --version
uv --version 2>/dev/null || echo "uv not installed"
```

### 2. Test Framework Detection

**Pytest Detection:**
- Check pyproject.toml: `grep -E '\[tool.pytest\]|\[tool.pytest.ini_options\]' pyproject.toml 2>/dev/null`
- Look for pytest config: `ls -la pytest.ini conftest.py setup.cfg 2>/dev/null`
- Check for test directories: `find . -type d -name "tests" -maxdepth 2 2>/dev/null`
- Check dependencies: `grep pytest pyproject.toml 2>/dev/null`

### 3. Dependency Validation

```bash
# Check if pytest is installed
uv pip list 2>/dev/null | grep pytest || pip list 2>/dev/null | grep pytest

# Check for coverage tools
uv pip list 2>/dev/null | grep -E "pytest-cov|coverage" || pip list 2>/dev/null | grep -E "pytest-cov|coverage"

# Check for other testing tools
uv pip list 2>/dev/null | grep -E "pytest-asyncio|pytest-mock|pytest-xdist" || pip list 2>/dev/null | grep -E "pytest-asyncio|pytest-mock|pytest-xdist"
```

If dependencies missing:
- Tell user: "❌ Test dependencies not installed"
- Suggest: "Run: uv pip install -e '.[test]' or pip install -e '.[test]'"

## Configuration Creation

### 1. Create Testing Configuration

Create `.claude/testing-config.md`:

```markdown
---
framework: pytest
test_command: uv run pytest
created: [Use REAL datetime from: date -u +"%Y-%m-%dT%H:%M:%SZ"]
---

# Python Testing Configuration

## Framework
- Type: pytest
- Version: [Get from: uv pip show pytest | grep Version]
- Config File: pyproject.toml

## Test Structure
- Test Directory: tests/
- Test Files: [Count from: find tests -name "test_*.py" | wc -l] files found
- Naming Pattern: test_*.py or *_test.py
- Fixtures: conftest.py

## Commands
- Run All Tests: `uv run pytest`
- Run with Coverage: `uv run pytest --cov={{cookiecutter.project_slug}} --cov-report=term-missing`
- Run Specific Test: `uv run pytest tests/test_specific.py`
- Run with Markers: `uv run pytest -m "not slow"`
- Run with Debugging: `uv run pytest -vvs --tb=long`
- Run Parallel: `uv run pytest -n auto` (if pytest-xdist installed)

## Environment
- PYTHONPATH: .
- Python Version: {{cookiecutter.python_version}}
- Package Manager: uv

## Coverage Settings
- Minimum Coverage: 80%
- Coverage Report: htmlcov/
- Exclude Patterns:
  - */tests/*
  - */migrations/*
  - */config/*

## Pytest Configuration (pyproject.toml)
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
    "--disable-warnings",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
```

## Test Runner Agent Configuration
- Use verbose output for debugging (-v)
- Run tests sequentially (no -n flag unless specified)
- Capture full stack traces (--tb=long when debugging)
- No mocking - use real implementations
- Use fixtures for test data
- Wait for each test to complete
```

### 2. Create Pytest Runner Agent

Create `.claude/agents/pytest-runner.md`:

```markdown
---
allowed-tools: Bash, Read
---

# Pytest Runner Agent

You are a specialized agent for running Python tests with pytest. Your role is to execute tests, analyze results, and provide actionable feedback.

## Core Responsibilities

1. **Test Execution**
   - Run pytest with appropriate options
   - Use uv for consistent environment
   - Capture full output for analysis
   - Handle test failures gracefully

2. **Result Analysis**
   - Parse test output for failures
   - Identify error patterns
   - Suggest fixes based on errors
   - Track coverage metrics

3. **Debugging Support**
   - Run failed tests with verbose output
   - Use --tb=long for full tracebacks
   - Isolate failing tests
   - Provide context for failures

## Execution Protocol

### 1. Pre-flight Checks
```bash
# Verify pytest is available
uv pip show pytest || echo "pytest not installed"

# Check for test files
find tests -name "test_*.py" | head -5

# Verify no syntax errors
python -m py_compile src/**/*.py 2>&1 | head -20
```

### 2. Test Execution

**Full Test Suite:**
```bash
uv run pytest -v --tb=short --strict-markers
```

**With Coverage:**
```bash
uv run pytest --cov={{cookiecutter.project_slug}} --cov-report=term-missing --cov-report=html
```

**Specific Test File:**
```bash
uv run pytest tests/test_specific.py -v
```

**Failed Tests Only:**
```bash
uv run pytest --lf -v  # Run last failed
uv run pytest --ff -v  # Run failed first
```

**Debug Mode:**
```bash
uv run pytest -vvs --tb=long --capture=no tests/test_failing.py
```

### 3. Output Analysis

Parse output for:
- Number of tests: passed, failed, skipped
- Failure reasons and locations
- Coverage percentage
- Slow test warnings
- Deprecation warnings

### 4. Failure Handling

For each failure:
1. Extract test name and location
2. Identify error type (assertion, exception, etc.)
3. Get relevant code context
4. Suggest specific fix
5. Verify fix doesn't break other tests

## Common Issues and Solutions

### Import Errors
- Check PYTHONPATH: `export PYTHONPATH=.`
- Verify package installed: `uv pip install -e .`
- Check __init__.py files exist

### Fixture Errors
- Verify conftest.py location
- Check fixture scope and dependencies
- Ensure fixture names match

### Async Test Issues
- Install pytest-asyncio: `uv pip install pytest-asyncio`
- Use @pytest.mark.asyncio decorator
- Check event loop configuration

### Coverage Issues
- Install pytest-cov: `uv pip install pytest-cov`
- Exclude test files from coverage
- Check .coveragerc configuration

## Reporting Format

```
🧪 Test Results
===============

📊 Summary:
- Total: X tests
- Passed: ✅ X
- Failed: ❌ X
- Skipped: ⏭️ X
- Coverage: X%

❌ Failures:
1. test_file.py::test_function
   Error: AssertionError: Expected X but got Y
   Location: line X
   Fix: [Specific suggestion]

📈 Coverage Report:
- Module A: X%
- Module B: X%
- Missing: [List uncovered lines]

💡 Recommendations:
- [Actionable suggestions]
```

## Best Practices

1. **Always use uv run** for consistent environment
2. **Start with -v** for visibility
3. **Use markers** to organize tests
4. **Run coverage** regularly
5. **Fix one test at a time**
6. **Verify fixes** don't break others
7. **Use fixtures** for test data
8. **Keep tests independent**
9. **Test edge cases**
10. **Document complex test logic**

Remember: The goal is not just to make tests pass, but to ensure they accurately test the code and reveal real issues.
```

### 3. Output Summary

After successful configuration:

```
🧪 Python Testing Environment Primed

🔍 Detection Results:
  ✅ Python: {{cookiecutter.python_version}}
  ✅ Package Manager: uv
  ✅ Framework: pytest [version]
  ✅ Test Files: [count] files in tests/
  ✅ Config: pyproject.toml
  ✅ Dependencies: All installed

📋 Test Structure:
  - Pattern: test_*.py
  - Directory: tests/
  - Fixtures: conftest.py
  - Coverage: pytest-cov configured

🤖 Agent Configuration:
  ✅ Pytest-runner agent configured
  ✅ Verbose output enabled
  ✅ Coverage tracking active
  ✅ Real implementations (no mocks)

⚡ Ready Commands:
  - Run all tests: /testing:run
  - Run with coverage: /testing:coverage
  - Run specific: /testing:run tests/test_file.py
  - Run failed only: /testing:run --lf

💡 Tips:
  - Use uv run for all commands
  - Check coverage regularly
  - Use fixtures for test data
  - Keep tests independent
```

## Error Handling

**No uv installed:**
- Message: "⚠️ uv not found, falling back to pip"
- Use: `pip` instead of `uv pip`
- Use: `python -m pytest` instead of `uv run pytest`

**No pytest installed:**
- Message: "❌ pytest not installed"
- Solution: "Install: uv pip install pytest pytest-cov"

**No test files:**
- Message: "⚠️ No test files found in tests/"
- Solution: "Create test files or check test directory"

**Import errors:**
- Message: "❌ Import errors detected"
- Solution: "Install package: uv pip install -e ."

## Important Notes

- **Always use uv run** when available
- **Configure in pyproject.toml** not separate files
- **Use fixtures** for all test data
- **Coverage minimum** 80% for critical code
- **Type hints** in test files too
- **Docstrings** for complex test logic

$ARGUMENTS