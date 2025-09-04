{% if cookiecutter.command_line_interface != "None" -%}
"""Tests for {{cookiecutter.project_name}} CLI."""

from __future__ import annotations

import subprocess
import sys
from unittest.mock import patch

import pytest

{% if cookiecutter.command_line_interface == "Typer" -%}
from typer.testing import CliRunner

from {{cookiecutter.project_slug}}.cli import app

runner = CliRunner()


def test_cli_help():
    """Test CLI help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "{{cookiecutter.project_short_description}}" in result.stdout


def test_cli_version():
    """Test CLI version command.""" 
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "{{cookiecutter.project_name}}" in result.stdout


def test_hello_command():
    """Test hello command."""
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Hello World!" in result.stdout


def test_hello_with_name():
    """Test hello command with custom name."""
    result = runner.invoke(app, ["hello", "Alice"])
    assert result.exit_code == 0
    assert "Hello Alice!" in result.stdout


def test_hello_with_count():
    """Test hello command with count option."""
    result = runner.invoke(app, ["hello", "--count", "3"])
    assert result.exit_code == 0
    assert result.stdout.count("Hello World!") == 3

{% elif cookiecutter.command_line_interface == "Click" -%}
from click.testing import CliRunner

from {{cookiecutter.project_slug}}.cli import main

runner = CliRunner()


def test_cli_help():
    """Test CLI help command."""
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "{{cookiecutter.project_short_description}}" in result.output


def test_cli_version():
    """Test CLI version command."""
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "{{cookiecutter.project_name}}" in result.output


def test_hello_command():
    """Test hello command."""
    result = runner.invoke(main, ["hello"])
    assert result.exit_code == 0
    assert "Hello World!" in result.output


def test_hello_with_name():
    """Test hello command with custom name."""
    result = runner.invoke(main, ["hello", "Alice"])
    assert result.exit_code == 0
    assert "Hello Alice!" in result.output


def test_hello_with_count():
    """Test hello command with count option."""
    result = runner.invoke(main, ["hello", "--count", "3"])
    assert result.exit_code == 0
    assert result.output.count("Hello World!") == 3

{% elif cookiecutter.command_line_interface == "argparse" -%}
from {{cookiecutter.project_slug}}.cli import main


def test_cli_help(capsys):
    """Test CLI help command."""
    with pytest.raises(SystemExit):
        main(["--help"])
    captured = capsys.readouterr()
    assert "{{cookiecutter.project_short_description}}" in captured.out


def test_cli_version(capsys):
    """Test CLI version command."""
    with pytest.raises(SystemExit):
        main(["--version"])
    captured = capsys.readouterr()
    assert "{{cookiecutter.project_name}}" in captured.out


def test_hello_command(capsys):
    """Test hello command."""
    result = main(["hello"])
    captured = capsys.readouterr()
    assert result == 0
    assert "Hello World!" in captured.out


def test_hello_with_name(capsys):
    """Test hello command with custom name."""
    result = main(["hello", "Alice"])
    captured = capsys.readouterr()
    assert result == 0
    assert "Hello Alice!" in captured.out


def test_hello_with_count(capsys):
    """Test hello command with count option."""
    result = main(["hello", "--count", "3"])
    captured = capsys.readouterr()
    assert result == 0
    assert captured.out.count("Hello World!") == 3


def test_no_command(capsys):
    """Test CLI with no command shows help."""
    result = main([])
    captured = capsys.readouterr()
    assert result == 1
    assert "usage:" in captured.out
{% endif %}


def test_cli_installed():
    """Test that CLI is properly installed."""
    result = subprocess.run(
        [sys.executable, "-m", "{{cookiecutter.project_slug}}.cli", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
{% endif %}