# CLAUDE.md

> Think carefully and implement the most concise solution that changes as little code as possible.

## CORE PRINCIPLE: NO VIBE CODING

> **Every line of code must trace back to a specification.**

We follow a strict 5-phase discipline:

1. **🧠 Brainstorm** - Think deeper than comfortable
2. **📝 Document** - Write specs that leave nothing to interpretation
3. **📐 Plan** - Architect with explicit technical decisions
4. **⚡ Execute** - Build exactly what was specified
5. **📊 Track** - Maintain transparent progress at every step

No shortcuts. No assumptions. No regrets.

## USE SUB-AGENTS FOR CONTEXT OPTIMIZATION

### 1. Always use the file-analyzer sub-agent when asked to read files.
The file-analyzer agent is an expert in extracting and summarizing critical information from files, particularly log files and verbose outputs. It provides concise, actionable summaries that preserve essential information while dramatically reducing context usage.

### 2. Always use the code-analyzer sub-agent when asked to search code, analyze code, research bugs, or trace logic flow.
The code-analyzer agent is an expert in code analysis, logic tracing, and vulnerability detection. It provides concise, actionable summaries that preserve essential information while dramatically reducing context usage.

### 3. Always use the test-runner sub-agent to run tests and analyze the test results.
Using the test-runner agent ensures:
- Full test output is captured for debugging
- Main conversation stays clean and focused
- Context usage is optimized
- All issues are properly surfaced
- No approval dialogs interrupt the workflow

### 4. For Python projects, use specialized agents:
- **ruff-analyzer** - For code quality and formatting analysis
- **mypy-checker** - For type checking and type inference
- **pytest-runner** - For test execution with fixture support
- **uv-manager** - For dependency management and virtual environments

## Philosophy

### Error Handling
- **Fail fast** for critical configuration (missing dependencies)
- **Log and continue** for optional features
- **Graceful degradation** when external services unavailable
- **User-friendly messages** through resilience layer

### Testing (Python-Specific)
- Always use the pytest-runner agent to execute tests
- Use `uv run pytest` for consistent environment
- Do not use mock services for anything ever
- Do not move on to the next test until the current test is complete
- If the test fails, check test structure before refactoring code
- Tests must be verbose for debugging (`pytest -v`)
- Use fixtures for test data, not inline data
- Coverage minimum: 80% for critical paths

### Code Quality (Python-Specific)
- Run `ruff check .` before any commit
- Run `ruff format .` for consistent formatting
- Run `mypy src/` for type checking
- Use `uv` for all package management
- Follow PEP 8 and existing project conventions

## Tone and Behavior
- Criticism is welcome. Tell me when I am wrong or mistaken
- Tell me if there is a better approach than the one I am taking
- Tell me if there is a relevant standard or convention I appear unaware of
- Be skeptical
- Be concise
- Short summaries are OK, but don't give extended breakdowns unless working through plan details
- Do not flatter or give compliments unless I ask for judgment
- Occasional pleasantries are fine
- Ask many questions. If in doubt of intent, don't guess. Ask.

## ABSOLUTE RULES:

### Code Implementation
- NO PARTIAL IMPLEMENTATION - Complete every feature fully
- NO SIMPLIFICATION - No "//This is simplified for now" comments
- NO CODE DUPLICATION - Check existing codebase to reuse functions and constants
- NO DEAD CODE - Either use or delete from codebase completely
- NO INCONSISTENT NAMING - Read existing codebase naming patterns
- NO OVER-ENGINEERING - Don't add unnecessary abstractions when simple functions work
- NO MIXED CONCERNS - Maintain proper separation of concerns
- NO RESOURCE LEAKS - Always clean up resources properly

### Testing Rules
- IMPLEMENT TEST FOR EVERY FUNCTION - No exceptions
- NO CHEATER TESTS - Tests must be accurate and reveal flaws
- USE PYTEST FIXTURES - For test data and setup
- TEST EDGE CASES - Always test boundary conditions
- VERBOSE OUTPUT - Design tests for debugging (`pytest -v`)

### Python-Specific Rules
- USE UV FOR PACKAGES - Never use pip directly
- TYPE EVERYTHING - Full type annotations required
- FOLLOW PYPROJECT.TOML - All config in one place
- USE SRC LAYOUT - Keep source in src/ directory
- DOCSTRINGS REQUIRED - For all public functions
- NO PRINT DEBUGGING - Use proper logging instead

### Project Management Rules
- SPEC BEFORE CODE - Write PRD/Epic before implementation
- TRACK EVERYTHING - Use PM commands for all work
- PARALLEL WHEN POSSIBLE - Mark tasks for parallel execution
- UPDATE REGULARLY - Sync progress to GitHub Issues
- CONTEXT PRESERVATION - Update .claude/context/ regularly