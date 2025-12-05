# Align installation instructions with uv (RESOLVED)

Installation guidance previously pointed to `pip`/`virtualenv` instead of the uv-first workflow used throughout the repo. This was updated in this PR to use uv consistently.

## Category

DOCUMENTATION

## Evidence

- Prior to this PR, README.md:184-215 and docs/README.md:172-203 described `pip3 install`, `virtualenv`, and editable installs even though the repository standards require uv for environment management.
- README.md:144-147 used `python3 -m http.server` directly while other commands relied on `uv run`, leaving the quickstart inconsistent about when uv was required.

## Resolution

1. Installation and development setup sections were rewritten to use `uv venv`/`uv sync` and `uv run` consistently, keeping `pip` only as an explicit fallback note if needed.
2. Local docs build and usage snippets were updated to show the uv workflow end-to-end (including serving docs/tests) so new users do not mix package managers.
3. A brief note was added about avoiding mixed `pip`/`uv` environments to prevent dependency drift.
