#!/usr/bin/env python
import os
import shutil
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

def main():
    """Post-generation cleanup and setup."""
    # Get configuration
    use_claude_pm = '{{ cookiecutter.use_claude_pm }}' == 'y'

    # If PM system is not enabled, remove .claude directory
    if not use_claude_pm:
        print("🧹 Removing Claude Code PM system files...")
        remove_directory('.claude')
        remove_file('COMMANDS.md')

if __name__ == '__main__':
    main()