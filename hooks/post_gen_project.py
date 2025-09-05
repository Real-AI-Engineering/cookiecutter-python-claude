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


def clean_empty_files():
    """Remove empty files that contain only whitespace or Jinja comments."""
    import os
    
    print("🧹 Cleaning empty files...")
    
    # Get project variables to know which files should exist
    project_type = "{{ cookiecutter.project_type }}"
    web_framework = "fastapi" if project_type != "cli" else "none"
    
    # Files that should never be removed for FastAPI projects
    fastapi_preserve_files = {
        "main.py",
        "health.py", 
        "router.py",
        "config.py",
        "logging.py",
        "item.py",
        "items.py",
        "item_service.py",
        "test_health.py",
        "test_main.py", 
        "test_items.py"
    }
    
    for root, dirs, files in os.walk("."):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.isfile(file_path):
                    # Skip preservation for FastAPI files when it's a web project
                    if web_framework == "fastapi" and any(preserve in file for preserve in fastapi_preserve_files):
                        continue
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        # Remove files that are empty or contain only Jinja comments
                        if not content or (content.startswith('{' + '%') and content.endswith('-' + '%}')):
                            os.remove(file_path)
                            print(f"  Removed empty file: {file_path}")
            except (UnicodeDecodeError, PermissionError):
                # Skip binary files or files we can't read
                continue


def clean_unused_files():
    """Remove files based on user choices."""
    print("🧹 Cleaning up unused files...")
    
    project_type = "{{ cookiecutter.project_type }}"
    
    # Evaluate computed variables manually
    web_framework = "fastapi" if project_type != "cli" else "none"
    use_structlog = "y" if project_type != "cli" else "n"
    
    
    # Files to potentially remove based on configuration
    conditional_files = [
        ("{{ cookiecutter.use_github_actions }}" != "y", ".github"),
        ("{{ cookiecutter.use_docker }}" != "y", "docker"),
        ("{{ cookiecutter.use_docker }}" != "y", ".dockerignore"),
        ("{{ cookiecutter.create_author_file }}" != "y", "AUTHORS.md"),
        # CLI-related files
        (project_type == "web", "src/{{ cookiecutter.project_slug }}/cli.py"),
        # FastAPI-related files
        (web_framework != "fastapi", "src/{{ cookiecutter.project_slug }}/main.py"),
        (web_framework != "fastapi", "src/{{ cookiecutter.project_slug }}/api"),
        (web_framework != "fastapi", "src/{{ cookiecutter.project_slug }}/models"),
        (web_framework != "fastapi", "src/{{ cookiecutter.project_slug }}/services"),
        (web_framework != "fastapi", "tests/test_health.py"),
        (web_framework != "fastapi", "tests/test_main.py"),
        (web_framework != "fastapi", "tests/test_items.py"),
        # Core files for non-web projects
        (project_type == "cli", "src/{{ cookiecutter.project_slug }}/core"),
        # Logging files
        (use_structlog != "y", "src/{{ cookiecutter.project_slug }}/core/logging.py"),
        # Remove empty template directory that shouldn't exist
        (True, "{{ cookiecutter.project_slug }}"),
    ]
    
    for condition, file_path in conditional_files:
        if condition and os.path.exists(file_path):
            remove_file_or_dir(file_path)
    
    # Clean up empty files that may have been created with only Jinja conditions
    clean_empty_files()


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
    
    project_type = "{{ cookiecutter.project_type }}"
    web_framework = "{{ cookiecutter._web_framework }}"
    
    # Common directories
    directories = [
        "tests/unit",
        "tests/integration",
        "tests/fixtures",
        "docs/api",
        "docs/guides",
        "docs/development",
        "scripts",
    ]
    
    # Add project-specific directories
    if project_type != "web":
        directories.extend([
            "src/{{ cookiecutter.project_slug }}/utils",
        ])
    
    if web_framework == "fastapi":
        # Ensure FastAPI specific directories exist
        directories.extend([
            "src/{{ cookiecutter.project_slug }}/api/v1/endpoints",
        ])
    
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
    project_type = "{{ cookiecutter.project_type }}"
    web_framework = "{{ cookiecutter._web_framework }}"
    use_pre_commit = "{{ cookiecutter.use_pre_commit }}" == "y"
    use_github_actions = "{{ cookiecutter.use_github_actions }}" == "y"
    use_docker = "{{ cookiecutter.use_docker }}" == "y"
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
    
    if web_framework == "fastapi":
        print(f"\n5. Start your FastAPI server:")
        print(f"   uvicorn {project_slug}.main:app --reload")
        print("   Then visit http://localhost:8000/docs for API documentation")
        print("   Health check: http://localhost:8000/healthz")
        
        if use_docker:
            print(f"\n6. Or run with Docker:")
            print("   cd docker && docker-compose up")
    
    elif cli_framework != "None":
        print(f"\n5. Try your CLI tool:")
        print(f"   python -m {project_slug}.cli --help")
    
    if use_github_actions:
        step_num = 7 if web_framework == "fastapi" and use_docker else 6
        print(f"\n{step_num}. Push to GitHub to trigger CI/CD:")
        print("   git remote add origin https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.pypi_package_name }}.git")
        print("   git push -u origin main")
    
    print(f"\n📖 Documentation:")
    print("   - CLAUDE.md: Instructions for Claude Code")
    print("   - AGENTS.md: Development workflow guidelines")
    print("   - README.md: Project overview and usage")
    
    if web_framework == "fastapi":
        print(f"\n🔧 FastAPI Features:")
        print("   - Kubernetes-style health endpoints (/healthz, /livez, /readyz)")
        print("   - Structured logging with correlation IDs")
        print("   - Pydantic v2 configuration management")
        print("   - Docker support with multi-stage builds")
        print("   - Comprehensive test suite")
    
    print(f"\n🚀 Happy coding with {project_name}!")


if __name__ == "__main__":
    print("🔧 Running post-generation setup...")
    
    clean_unused_files()
    create_additional_directories()
    setup_pre_commit()
    initialize_git_repo()
    print_next_steps()