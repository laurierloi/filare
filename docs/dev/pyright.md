# Pyright type checking

Filare ships a lightweight Pyright setup to spot typing regressions without blocking development.

## Configuration
- Location: `[tool.pyright]` in `pyproject.toml`.
- Defaults: Python 3.9, typeCheckingMode `basic`, include `src/`, exclude build/temp dirs (`report`, `outputs`, `.uv-cache`, `.venv`), `reportMissingImports: warning`.
- Uses project virtualenv `.venv` (set via `venvPath`/`venv`).

## Installing tools
```bash
uv venv
uv sync --group dev
```

## Running Pyright
```bash
./scripts/pyright.sh [pyright args...]
```
- Uses `UV_CACHE_DIR` (defaults to `.uv-cache`) and project pyproject config.
- Pass additional flags to focus on paths or enable stricter checks if needed.

## Workflow tips
- Run Pyright before submitting refactors to catch type drift early.
- For now, fixing warnings is optional; the goal is to surface issues. Treat new warnings as follow-ups in your PR description if you defer fixes.
