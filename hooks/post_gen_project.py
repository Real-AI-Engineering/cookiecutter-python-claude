#!/usr/bin/env python
"""Post-generation hook to clean up unused files and initialize project."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def remove_file_or_dir(path):
    """Remove file or directory if it exists."""
    if os.path.isfile(path):
        os.remove(path)
        print(f"  Removed file: {path}")
    elif os.path.isdir(path):
        shutil.rmtree(path)
        print(f"  Removed directory: {path}")


def clean_unused_files():
    """Remove files based on user choices."""
    print("🧹 Cleaning up unused files...")
    
    # Files to potentially remove based on configuration
    conditional_files = [
        ("{{ cookiecutter.use_github_actions }}" != "y", ".github"),
        ("{{ cookiecutter.use_docker }}" != "y", "Dockerfile"),
        ("{{ cookiecutter.use_docker }}" != "y", ".dockerignore"),
        ("{{ cookiecutter.use_docker }}" != "y", "docker-compose.yml"),
        ("{{ cookiecutter.create_author_file }}" != "y", "AUTHORS.md"),
        ("{{ cookiecutter.command_line_interface }}" == "None", "src/{{ cookiecutter.project_slug }}/cli.py"),
    ]
    
    for condition, file_path in conditional_files:
        if condition and os.path.exists(file_path):
            remove_file_or_dir(file_path)


def initialize_git_repo():
    """Initialize git repository if git is available."""
    try:
        print("🔧 Initializing git repository...")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run([
            "git", "commit", "-m", 
            "Initial commit: Generated project from cookiecutter template"
        ], check=True, capture_output=True)
        print("  ✅ Git repository initialized with initial commit")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ⚠️  Git not available or failed to initialize repository")


def setup_pre_commit():
    """Set up pre-commit hooks if requested."""
    if "{{ cookiecutter.use_pre_commit }}" == "y":
        try:
            print("🔧 Setting up pre-commit hooks...")
            
            # Create .pre-commit-config.yaml if it doesn't exist
            pre_commit_config = Path(".pre-commit-config.yaml")
            if not pre_commit_config.exists():
                config_content = """# See https://pre-commit.com for more information
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: pretty-format-json
        args: ['--autofix']
      - id: check-merge-conflict
      - id: check-case-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]
"""
                pre_commit_config.write_text(config_content)
                print("  ✅ Created .pre-commit-config.yaml")
            
            # Try to install pre-commit hooks
            subprocess.run(["pre-commit", "install"], check=True, capture_output=True)
            print("  ✅ Pre-commit hooks installed")
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  ⚠️  Pre-commit not available. Install with: pip install pre-commit")


def create_additional_directories():
    """Create additional directories that might be needed."""
    print("📁 Creating additional directories...")
    
    directories = [
        "src/{{ cookiecutter.project_slug }}/core",
        "src/{{ cookiecutter.project_slug }}/utils", 
        "tests/unit",
        "tests/integration",
        "tests/fixtures",
        "docs/api",
        "docs/guides",
        "docs/development",
        "scripts",
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
        # Create __init__.py files in Python packages
        if directory.startswith("src/") or directory.startswith("tests/"):
            init_file = Path(directory) / "__init__.py"
            if not init_file.exists():
                init_file.touch()


def print_next_steps():
    """Print helpful next steps for the user."""
    project_name = "{{ cookiecutter.project_name }}"
    project_slug = "{{ cookiecutter.project_slug }}"
    use_pre_commit = "{{ cookiecutter.use_pre_commit }}" == "y"
    use_github_actions = "{{ cookiecutter.use_github_actions }}" == "y"
    cli_framework = "{{ cookiecutter.command_line_interface }}"
    
    print("\n" + "="*60)
    print(f"🎉 Successfully created '{project_name}' project!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Create and activate a virtual environment:")
    print("   python -m venv venv")
    print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("\n2. Install the project in development mode:")
    print('   pip install -e ".[dev]"')
    
    if use_pre_commit:
        print("\n3. Pre-commit hooks are ready! Run checks with:")
        print("   pre-commit run --all-files")
    
    print(f"\n4. Run tests to verify everything works:")
    print("   pytest")
    
    if cli_framework != "None":
        print(f"\n5. Try your CLI tool:")
        print(f"   python -m {project_slug}.cli --help")
    
    if use_github_actions:
        print(f"\n6. Push to GitHub to trigger CI/CD:")
        print("   git remote add origin https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.pypi_package_name }}.git")
        print("   git push -u origin main")
    
    print(f"\n📖 Documentation:")
    print("   - CLAUDE.md: Instructions for Claude Code")
    print("   - AGENTS.md: Development workflow guidelines")
    print("   - README.md: Project overview and usage")
    
    print(f"\n🚀 Happy coding with {project_name}!")


if __name__ == "__main__":
    print("🔧 Running post-generation setup...")
    
    clean_unused_files()
    create_additional_directories()
    setup_pre_commit()
    initialize_git_repo()
    print_next_steps()