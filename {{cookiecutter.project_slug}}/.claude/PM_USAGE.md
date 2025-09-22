# Claude Code PM System - Usage Guide

## 🚀 Quick Start

### Initial Setup
```bash
# 1. Initialize the PM system
bash .claude/init.sh

# 2. Plan your first epic
.claude/scripts/pm/epic-plan

# 3. Start your first task
.claude/scripts/pm/task-start
```

## 📋 Core PM Commands

### Epic Management
```bash
# Plan a new epic with GitHub issue creation
.claude/scripts/pm/epic-plan

# View current epic status
.claude/scripts/pm/epic-status

# Complete an epic
.claude/scripts/pm/epic-complete
```

### Task Management
```bash
# Start a new task (creates worktree)
.claude/scripts/pm/task-start

# Complete current task (merges to main)
.claude/scripts/pm/task-complete

# Update task progress
.claude/scripts/pm/task-update

# Block a task with reason
.claude/scripts/pm/task-block "Waiting for API specs"
```

### Progress Tracking
```bash
# Generate progress report
.claude/scripts/pm/progress-report

# Sync with GitHub issues
.claude/scripts/pm/sync-github

# View all tasks status
.claude/scripts/pm/status
```

## 🐍 Python-Specific Commands

### Testing & Quality
```bash
# Run comprehensive test suite
/testing:prime-python

# Check dependencies for vulnerabilities
/pm:deps-check

# Fix code formatting and linting
/pm:lint-fix

# Generate coverage report
/pm:coverage-report
```

### Development Tools
```bash
# Create new module with tests
/pm:module-create my_module

# Generate type stubs
/pm:type-stubs

# Profile performance
/pm:profile-code

# Check for security issues
/pm:security-check
```

### Documentation
```bash
# Generate API documentation
/pm:docs-gen

# Create changelog
/pm:changelog-gen
```

## 🤖 Using Agents

### Python Testing Agent
```
# In Claude Code, use the Task tool:
Task: Run all tests using pytest-runner agent. Focus on integration tests and report coverage gaps.
```

### Code Analysis Agent
```
Task: Use code-analyzer agent to review the auth module for security vulnerabilities and performance issues.
```

### Documentation Agent
```
Task: Use docs-generator agent to create comprehensive API documentation for all public modules.
```

## 📝 Epic Planning Workflow

### 1. Create Epic Specification
```bash
# Start planning
.claude/scripts/pm/epic-plan

# This will:
# - Create PRD document
# - Generate task breakdown
# - Create GitHub issue
# - Set up epic directory
```

### 2. Epic Directory Structure
```
.claude/epics/auth-system/
├── PRD.md           # Product Requirements
├── tasks.md         # Task breakdown
├── progress.md      # Progress tracking
├── .env             # Epic-specific config
└── tests/           # Epic-specific tests
```

### 3. Working with Tasks
```bash
# Start task from epic
.claude/scripts/pm/task-start

# Select task number from list
# Creates Git worktree in .claude/epics/[epic]/tasks/[task]

# Work on the task...

# Complete and merge
.claude/scripts/pm/task-complete
```

## 🔄 Parallel Development

### Using Git Worktrees
```bash
# Tasks automatically use worktrees
.claude/scripts/pm/task-start
# Creates: .claude/epics/auth/tasks/task-001-setup/

# Work on multiple tasks simultaneously
.claude/scripts/pm/task-parallel task1 task2 task3
```

### Managing Worktrees
```bash
# List all worktrees
git worktree list

# Clean up completed worktrees
.claude/scripts/pm/worktree-cleanup
```

## 📊 Progress Reporting

### Generate Reports
```bash
# Full progress report
.claude/scripts/pm/progress-report

# Outputs:
# - Completed tasks
# - In-progress items
# - Blocked tasks
# - Burndown chart
# - Time estimates
```

### GitHub Integration
```bash
# Sync progress to GitHub
.claude/scripts/pm/sync-github

# Updates:
# - Issue progress
# - Task checkboxes
# - Labels
# - Milestones
```

## 🎯 Best Practices

### 1. Start Every Session
```bash
# Check status first
.claude/scripts/pm/status

# Review blocked tasks
.claude/scripts/pm/blocked-tasks

# Continue where you left off
.claude/scripts/pm/task-resume
```

### 2. Atomic Commits
```bash
# Each task = one feature
# Each commit = one logical change
# Use conventional commits:
git commit -m "feat: add user authentication"
git commit -m "fix: resolve memory leak in cache"
git commit -m "docs: update API examples"
```

### 3. Test-Driven Development
```bash
# 1. Write test first
/pm:test-create test_new_feature

# 2. Run test (should fail)
/testing:prime-python

# 3. Implement feature
# 4. Run test (should pass)
# 5. Commit both together
```

### 4. Documentation as Code
```bash
# Keep docs in sync
/pm:docs-gen

# Update PRD when requirements change
vim .claude/epics/current/PRD.md

# Generate changelog before release
/pm:changelog-gen
```

## 🚨 Troubleshooting

### Common Issues

**Issue**: Task won't complete
```bash
# Check for uncommitted changes
git status

# Force complete if needed
.claude/scripts/pm/task-complete --force
```

**Issue**: Worktree conflicts
```bash
# List worktrees
git worktree list

# Remove broken worktree
git worktree remove .claude/epics/[epic]/tasks/[task] --force
```

**Issue**: GitHub sync fails
```bash
# Check GitHub token
echo $GITHUB_TOKEN

# Set token if missing
export GITHUB_TOKEN="your-token"

# Retry sync
.claude/scripts/pm/sync-github
```

## 📚 Advanced Usage

### Custom Commands
Create your own PM commands in `.claude/commands/custom/`:

```bash
# .claude/commands/custom/my-command.md
#!/bin/bash
echo "Running custom command..."
# Your logic here
```

### Hooks
Add pre/post hooks for PM commands:

```bash
# .claude/hooks/pre-task-start.sh
echo "Setting up environment..."

# .claude/hooks/post-task-complete.sh
echo "Cleaning up..."
```

### Context Preservation
```bash
# Save current context
.claude/scripts/pm/context-save

# Restore context in new session
.claude/scripts/pm/context-restore
```

## 🔗 Integration with Claude Code

When using Claude Code (claude.ai/code), mention PM commands directly:
- "Run /testing:prime-python to test everything"
- "Use epic-plan to start new feature"
- "Execute task-complete to finish current work"

Claude Code will recognize and execute these commands automatically.

## 📖 Further Reading

- [CLAUDE.md](.claude/CLAUDE.md) - Core principles and rules
- [AGENTS.md](.claude/AGENTS.md) - Available AI agents
- [commands/](.claude/commands/) - All available commands
- [scripts/pm/](.claude/scripts/pm/) - PM script sources