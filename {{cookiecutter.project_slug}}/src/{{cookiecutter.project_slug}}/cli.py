{% if cookiecutter.command_line_interface != "None" -%}
"""Command-line interface for {{cookiecutter.project_name}}."""

from __future__ import annotations

{% if cookiecutter.command_line_interface == "Typer" -%}
import typer
from typing_extensions import Annotated

from {{cookiecutter.project_slug}} import __version__

app = typer.Typer(
    name="{{cookiecutter.project_slug}}",
    help="{{cookiecutter.project_short_description}}",
    no_args_is_help=True,
)


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        typer.echo(f"{{cookiecutter.project_name}} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit.",
        ),
    ] = False,
) -> None:
    """{{cookiecutter.project_name}} CLI."""
    pass


@app.command()
def hello(
    name: Annotated[str, typer.Argument(help="Name to greet")] = "World",
    count: Annotated[int, typer.Option(help="Number of greetings")] = 1,
) -> None:
    """Say hello to someone."""
    for _ in range(count):
        typer.echo(f"Hello {name}!")


if __name__ == "__main__":
    app()

{% elif cookiecutter.command_line_interface == "Click" -%}
import click

from {{cookiecutter.project_slug}} import __version__


@click.group()
@click.version_option(version=__version__, prog_name="{{cookiecutter.project_name}}")
@click.pass_context
def main(ctx: click.Context) -> None:
    """{{cookiecutter.project_short_description}}."""
    ctx.ensure_object(dict)


@main.command()
@click.argument("name", default="World")
@click.option("--count", default=1, help="Number of greetings.")
def hello(name: str, count: int) -> None:
    """Say hello to someone."""
    for _ in range(count):
        click.echo(f"Hello {name}!")


if __name__ == "__main__":
    main()

{% elif cookiecutter.command_line_interface == "argparse" -%}
import argparse
import sys
from typing import Sequence

from {{cookiecutter.project_slug}} import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="{{cookiecutter.project_slug}}",
        description="{{cookiecutter.project_short_description}}",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{{cookiecutter.project_name}} v{__version__}",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Hello command
    hello_parser = subparsers.add_parser("hello", help="Say hello to someone")
    hello_parser.add_argument("name", nargs="?", default="World", help="Name to greet")
    hello_parser.add_argument("--count", type=int, default=1, help="Number of greetings")
    
    return parser


def cmd_hello(args: argparse.Namespace) -> None:
    """Say hello to someone."""
    for _ in range(args.count):
        print(f"Hello {args.name}!")


def main(argv: Sequence[str] | None = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == "hello":
        cmd_hello(args)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
{% endif %}
{% endif %}