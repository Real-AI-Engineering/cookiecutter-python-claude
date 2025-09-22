#!/usr/bin/env python
import os
import shutil
import subprocess
import sys
from pathlib import Path

def remove_file(filepath):
    """Remove a file if it exists."""
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"  Removed file: {filepath}")

def remove_directory(dirpath):
    """Remove a directory and its contents if it exists."""
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
        print(f"  Removed directory: {dirpath}")

def run_command(cmd, description=None):
    """Run a shell command and return success status."""
    if description:
        print(f"  {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"  ⚠️ Command failed: {e}")
        return False

def main():
    """Post-generation cleanup and setup."""
    # Get configuration
    use_claude_pm = '{{ cookiecutter.use_claude_pm }}' == 'y'
    github_username = '{{ cookiecutter.github_username }}'
    pypi_package_name = '{{ cookiecutter.pypi_package_name }}'

    # If PM system is not enabled, remove .claude directory
    if not use_claude_pm:
        print("🧹 Removing Claude Code PM system files...")
        remove_directory('.claude')
        remove_file('COMMANDS.md')
    else:
        print("🚀 Setting up Claude Code PM system...")

        # Initialize git if not already
        if not os.path.exists('.git'):
            run_command('git init', 'Initializing Git repository')

        # Set up GitHub remote if not exists
        remote_exists = run_command('git remote get-url origin', None)
        if not remote_exists:
            github_url = f"https://github.com/{github_username}/{pypi_package_name}.git"
            run_command(f'git remote add origin {github_url}', f'Adding GitHub remote: {github_url}')

        # Make PM scripts executable
        if os.path.exists('.claude/scripts/pm'):
            run_command('chmod +x .claude/scripts/pm/*.sh', 'Making PM scripts executable')

        # Create initial context directory
        os.makedirs('.claude/context', exist_ok=True)

        # Create a Python-specific init script runner
        init_runner = Path('.claude/scripts/init-python.sh')
        init_runner.parent.mkdir(exist_ok=True)
        init_runner.write_text("""#!/bin/bash
# Python-specific initialization

echo "🐍 Python Project Initialization"
echo "================================"

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "🔧 Creating virtual environment..."
    uv venv
fi

# Install dependencies
echo "📦 Installing dependencies..."
source .venv/bin/activate
uv pip install -e ".[dev,test]"

# Install pre-commit hooks if available
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🔗 Installing pre-commit hooks..."
    pre-commit install
fi

echo "✅ Python environment ready!"
echo ""
echo "Next steps:"
echo "1. Run: source .venv/bin/activate"
echo "2. Run: /pm:init to complete PM setup"
echo "3. Create your first PRD: /pm:prd-new <feature-name>"
""")
        init_runner.chmod(0o755)

        print("\n✅ Claude Code PM system configured!")
        print("\n📋 Next steps:")
        print("  1. Open project in Claude Code")
        print("  2. Run: /pm:init")
        print("  3. Run: /context:create")
        print("  4. Start with: /pm:prd-new <feature-name>")
        print("\n💡 For Python-specific commands, see:")
        print("  .claude/commands/pm/python-commands.md")

if __name__ == '__main__':
    main()