# Commands

{% if cookiecutter.use_claude_pm == "y" -%}
Complete reference of all commands available in the Claude Code PM system.

> **Note**: For a quick summary of commands, type `/pm:help` in Claude Code.

## Table of Contents

- [Project Management Commands](#project-management-commands)
- [Context Commands](#context-commands)
- [Testing Commands](#testing-commands)
- [Utility Commands](#utility-commands)
- [Review Commands](#review-commands)

## Project Management Commands

Commands for managing PRDs, epics, and issues using GitHub as the source of truth.

### Initial Setup
- `/pm:init` - Install dependencies and configure GitHub

### PRD Commands
- `/pm:prd-new` - Launch brainstorming for new product requirement
- `/pm:prd-parse` - Convert PRD to implementation epic
- `/pm:prd-list` - List all PRDs
- `/pm:prd-edit` - Edit existing PRD
- `/pm:prd-status` - Show PRD implementation status

### Epic Commands
- `/pm:epic-decompose` - Break epic into task files
- `/pm:epic-sync` - Push epic and tasks to GitHub
- `/pm:epic-oneshot` - Decompose and sync in one command
- `/pm:epic-list` - List all epics
- `/pm:epic-show` - Display epic and its tasks
- `/pm:epic-close` - Mark epic as complete
- `/pm:epic-edit` - Edit epic details
- `/pm:epic-refresh` - Update epic progress from tasks

### Issue Commands
- `/pm:issue-show` - Display issue and sub-issues
- `/pm:issue-status` - Check issue status
- `/pm:issue-start` - Begin work with specialized agent
- `/pm:issue-sync` - Push updates to GitHub
- `/pm:issue-close` - Mark issue as complete
- `/pm:issue-reopen` - Reopen closed issue
- `/pm:issue-edit` - Edit issue details

### Workflow Commands
- `/pm:next` - Show next priority issue with epic context
- `/pm:status` - Overall project dashboard
- `/pm:standup` - Daily standup report
- `/pm:blocked` - Show blocked tasks
- `/pm:in-progress` - List work in progress

### Sync Commands
- `/pm:sync` - Full bidirectional sync with GitHub
- `/pm:import` - Import existing GitHub issues

### Maintenance Commands
- `/pm:validate` - Check system integrity
- `/pm:clean` - Archive completed work
- `/pm:search` - Search across all content

## Context Commands

Commands for managing project context in `.claude/context/`.

### `/context:create`
- **Purpose**: Create initial project context documentation
- **Usage**: `/context:create`
- **Description**: Analyzes the project structure and creates comprehensive baseline documentation
- **When to use**: At project start or when context needs full rebuild

### `/context:update`
- **Purpose**: Update existing context with recent changes
- **Usage**: `/context:update`
- **Description**: Refreshes context documentation based on recent code changes
- **When to use**: After significant changes or before major work sessions

### `/context:prime`
- **Purpose**: Load context into current conversation
- **Usage**: `/context:prime`
- **Description**: Reads all context files and loads them into memory
- **When to use**: At the start of any work session

## Testing Commands

Commands for test configuration and execution.

### `/testing:prime`
- **Purpose**: Configure testing setup
- **Usage**: `/testing:prime`
- **Description**: Detects and configures the project's testing framework
- **When to use**: Initial project setup or when testing framework changes

### `/testing:run`
- **Purpose**: Execute tests with intelligent analysis
- **Usage**: `/testing:run [test_target]`
- **Description**: Runs tests using the test-runner agent
- **Options**:
  - No arguments: Run all tests
  - File path: Run specific test file
  - Pattern: Run tests matching pattern

## Utility Commands

General utility and maintenance commands.

### `/prompt`
- **Purpose**: Handle complex prompts with multiple references
- **Usage**: Write your prompt in the file, then type `/prompt`
- **Description**: Ephemeral command for complex prompts
- **When to use**: When Claude's UI rejects complex prompts

### `/re-init`
- **Purpose**: Update or create CLAUDE.md with PM rules
- **Usage**: `/re-init`
- **Description**: Updates the project's CLAUDE.md file
- **When to use**: After cloning PM system or updating rules

## Review Commands

Commands for handling external code review tools.

### `/code-rabbit`
- **Purpose**: Process CodeRabbit review comments intelligently
- **Usage**: `/code-rabbit` then paste comments
- **Description**: Evaluates suggestions with context awareness
- **Features**:
  - Accepts: Real bugs, security issues, resource leaks
  - Ignores: Style preferences, irrelevant patterns
  - Parallel processing for multiple files

## Command Patterns

All commands follow consistent patterns:

### Allowed Tools
Each command specifies its required tools in frontmatter:
- `Read, Write, LS` - File operations
- `Bash` - System commands
- `Task` - Sub-agent spawning
- `Grep` - Code searching

### Error Handling
Commands follow fail-fast principles:
- Check prerequisites first
- Clear error messages with solutions
- Never leave partial state

### Context Preservation
Commands that process lots of information:
- Use agents to shield main thread from verbose output
- Return summaries, not raw data
- Preserve only essential information

{% else -%}
This project does not have the Claude Code PM system enabled.

To enable it, regenerate the project with `use_claude_pm: y` option.
{% endif -%}

## Standard Development Commands

### Code Quality
```bash
# Format code with ruff
ruff format .

# Lint and auto-fix issues
ruff check . --fix

# Type checking with mypy
mypy src/
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov={{cookiecutter.project_slug}} --cov-report=html

# Run specific test
pytest tests/test_specific.py
```

{% if cookiecutter.use_pre_commit == "y" -%}
### Pre-commit Hooks
```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files

# Update hook versions
pre-commit autoupdate
```
{% endif -%}

{% if cookiecutter.use_docker == "y" -%}
### Docker
```bash
# Build production image
docker build -f docker/Dockerfile -t {{cookiecutter.project_slug}}:latest .

# Run container
docker run -p 8000:8000 {{cookiecutter.project_slug}}:latest

# Development with docker-compose
cd docker && docker-compose up
```
{% endif -%}

See [AGENTS.md](AGENTS.md) for more development workflow guidelines.