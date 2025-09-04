#!/usr/bin/env python
"""Pre-generation hook to validate user inputs."""

import re
import sys
import keyword


def validate_project_slug():
    """Validate that project slug is a valid Python module name."""
    module_regex = r"^[_a-zA-Z][_a-zA-Z0-9]*$"
    project_slug = "{{ cookiecutter.project_slug }}"
    
    if not re.match(module_regex, project_slug):
        print(
            f"ERROR: The project slug '{project_slug}' is not a valid Python module name.\n"
            "Please ensure it:\n"
            "- Starts with a letter or underscore\n"
            "- Contains only letters, numbers, and underscores\n"
            "- Does not contain hyphens or spaces"
        )
        sys.exit(1)
    
    if keyword.iskeyword(project_slug):
        print(
            f"ERROR: The project slug '{project_slug}' is a Python reserved keyword.\n"
            "Please choose a different name."
        )
        sys.exit(1)


def validate_pypi_package_name():
    """Validate PyPI package name format."""
    package_name_regex = r"^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$"
    package_name = "{{ cookiecutter.pypi_package_name }}"
    
    if not re.match(package_name_regex, package_name):
        print(
            f"ERROR: The PyPI package name '{package_name}' is not valid.\n"
            "Please ensure it:\n"
            "- Starts and ends with alphanumeric characters\n"
            "- Can contain letters, numbers, hyphens, underscores, and periods\n"
            "- Does not start or end with special characters"
        )
        sys.exit(1)
    
    if len(package_name) > 214:
        print(
            f"ERROR: The PyPI package name '{package_name}' is too long (>{214} characters).\n"
            "Please choose a shorter name."
        )
        sys.exit(1)


def validate_python_version():
    """Validate Python version format."""
    python_version = "{{ cookiecutter.python_version }}"
    version_regex = r"^3\.(1[0-3]|[6-9])$"
    
    if not re.match(version_regex, python_version):
        print(
            f"ERROR: Python version '{python_version}' is not supported.\n"
            "Please choose from: 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13"
        )
        sys.exit(1)


def validate_email():
    """Basic email validation."""
    email = "{{ cookiecutter.email }}"
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    if not re.match(email_regex, email):
        print(
            f"WARNING: The email address '{email}' might not be valid.\n"
            "Please double-check the format."
        )


if __name__ == "__main__":
    print("🔍 Validating project configuration...")
    
    validate_project_slug()
    validate_pypi_package_name() 
    validate_python_version()
    validate_email()
    
    print("✅ Project configuration is valid!")