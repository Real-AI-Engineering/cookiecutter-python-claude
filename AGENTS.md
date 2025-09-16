# Repository Guidelines

## Project Structure & Module Organization
The root holds `cookiecutter.json` for interactive prompts, `hooks/` for pre/post generation scripts, and the `{{cookiecutter.project_slug}}/` template rendered for each project. Inside the template keep `src/` for package code, `tests/`, `docs/`, `docker/`, and configuration files such as `pyproject.toml` and `CLAUDE.md`. Edit Jinja placeholders carefully so every variant renders correctly.

## Build, Test, and Development Commands
```bash
python -m venv .venv && source .venv/bin/activate   # local tooling env
pip install -U cookiecutter tox                     # install template deps
cookiecutter .                                      # generate a smoke-test project
cd my-sample && pip install -e ".[dev]"            # install generated project
ruff check . && ruff format --check .               # lint/format verification
pytest && pytest --cov                              # run test suite + coverage
```
Repeat the pytest step under each supported interpreter (for example, using `pyenv local 3.10 3.11 3.12` or the CI matrix) when validating multi-version support.

## Coding Style & Naming Conventions
Prefer four-space indentation, `snake_case` modules and functions, and `PascalCase` classes. Generated projects rely on `ruff` (line length 88) for linting/formatting, `black` compatibility, and `mypy`/`pyright` for strict type checking—keep the corresponding `[tool.*]` blocks synchronized when modifying `pyproject.toml`. Keep template module docstrings concise and favor pure functions inside `src/{{cookiecutter.project_slug}}/core/` and FastAPI routers under `api/`.

## Testing Guidelines
Every change should be exercised by creating at least one sample project covering the relevant options (CLI-only, web-only, or both). Run `pytest` and `pytest --cov={{cookiecutter.project_slug}}` inside the generated repo, and execute `ruff check` plus `mypy src/` to catch template regressions. When editing hooks, add manual spot checks to ensure files are removed or retained as expected. Place shared fixtures in `tests/conftest.py` or a dedicated helper module, and follow `test_<feature>.py` naming.

## Commit & Pull Request Guidelines
Commits follow a Conventional Commit prefix (`feat:`, `docs:`, `fix:`) as seen in history—use present tense and keep messages under 72 characters. PRs should describe the cookiecutter option(s) touched, reference any related issues, and paste the commands you ran (generation, lint, tests). Include screenshots or logs when CI-impacting changes are proposed, and mention if additional template variants still need coverage.

## Hooks & Template Maintenance
When updating `hooks/`, ensure they remain idempotent and safe for all project types. Guard new removals behind configuration checks, and document defaults in `cookiecutter.json` so prompt text and logic stay aligned. Review rendered output for Unicode or platform-specific paths before merging.
