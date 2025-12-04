# Align installation instructions with uv
Installation guidance still points to `pip`/`virtualenv` instead of the uv-first workflow used throughout the repo.

## Category
DOCUMENTATION

## Evidence
- README.md:184-215 and docs/README.md:172-203 describe `pip3 install`, `virtualenv`, and editable installs even though the repository standards require uv for environment management.
- README.md:144-147 uses `python3 -m http.server` directly while other commands rely on `uv run`, leaving the quickstart inconsistent about when uv is required.

## Suggested Next Steps
1. Rewrite installation and development setup sections to use `uv venv`/`uv sync` and `uv run` consistently, keeping `pip` only as an explicit fallback note if needed.
2. Update the local docs build and usage snippets to show the uv workflow end-to-end (including serving docs/tests) so new users do not mix package managers.
3. Add a brief note about avoiding mixed `pip`/`uv` environments to prevent dependency drift.
