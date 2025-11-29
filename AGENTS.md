# Repository Guidelines

## Project Structure & Module Organization
- Core library and CLI live in `src/filare/`; `wv_cli.py` exposes `filare`/`filare-qty`, with rendering and BOM logic in `wv_graphviz.py`, `wv_output.py`, and helpers under `tools/`.
- Documentation is under `docs/` (see `docs/README.md` and `docs/syntax.md`), with walkthroughs in `tutorial/` and ready-made YAML inputs in `examples/`.
- Architecture/data-flow/model diagrams live in `docs/graphs/`; update the Mermaid sources and regenerate rendered outputs when code structure changes.
- Regression YAMLs live in `tests/rendering/` and `tests/bom/`; write generated outputs to `outputs/` or a temp directory.
- Harness definitions for XSC live next door in `../xsc-harnesses`; treat them as downstream consumers built with the same Filare venv.

## Build, Test, and Development Commands
- Always use the uv package manager for Python (env, installs, and command execution):
  - First-time bootstrap (or when deps change): `uv venv; uv sync`
  - Create venv: `uv venv` # Create venv before running any other command
  - Add a package: `uv add <package>`
  - Install all packages `uv venv; uv sync`
  - Run a Python entrypoint or script: `uv venv; uv run <command>`
  - Run tests/coverage: `uv run pytest`
  - Avoid `pip`, `python -m venv`, or direct `python`/`pytest` calls; route everything through `uv venv`/`uv run`.
- Quick sanity run: `uv venv; uv sync; uv run filare examples/demo01.yml -f hpst -o outputs` (HTML/PNG/SVG/TSV). Add `-c examples/components.yml` or `-d metadata.yml` as needed.
- Build downstream harnesses with the same venv: `cd ../xsc-harnesses && WIREVIZ=../Filare-codex1/.venv/bin/filare make`; `make clean` removes generated SVG/PNG/PDF/TSV.
- For manual BOM scaling checks: `uv venv; uv run filare-qty tests/bom/bomqty.yml --use-qty-multipliers`.
- Keep `scripts/pre-commit.sh` aligned with CI: it must build a fresh uv venv, install deps, run black, prettier, pytest, and the example builds before you commit.
- Before committing, also generate examples to match CI: `uv venv; uv sync --group dev; uv run --no-sync filare -f hs -o outputs/examples examples/demo01.yml && uv run --no-sync filare -f h -o outputs/tutorial tutorial/tutorial01.yml`.

## Coding Style & Naming Conventions
- Python 3.9+; 4-space indentation; follow existing naming (modules, lowercase functions).
- Format with Black and organize imports with isort. Run `./cleanup.sh` to apply autoflake + isort + black across `src/filare/`.
- Docstrings follow Google style; keep CLI help strings succinct and user-facing.
- Template and asset names stay lowercase with hyphens or underscores; keep YAML keys lowercase.
- Keep docs coherent with code: when modifying metadata, flows, parser, or render behavior, update `docs/`, `docs/dev/`, and `docs/graphs/` accordingly (metadata guides, syntax, diagrams).

## Testing Guidelines
- No full automated test harness is wired up; use YAMLs in `tests/` and `examples/` to spot rendering/BOM regressions.
- Add a minimal YAML in `tests/rendering/` or `tests/bom/` for new behavior; keep file names numeric-prefixed (`04_newfeature.yml`).
- Also build the XSC harness suite with the project venv (`cd ../xsc-harnesses && WIREVIZ=../Filare-codex1/venv-filare/bin/filare make`) to catch downstream breakage.
- Ensure GraphViz (`dot -V`) and required fonts are available before debugging rendering differences.

## Commit & Pull Request Guidelines
- Open an issue first, then branch from `dev`. Use imperative, concise commit subjects and reference the issue number in the body when applicable.
- Base PRs on `dev`; describe the user-visible change, mention new YAML examples/tests (including any XSC harness updates), and link related issues. Update `docs/syntax.md` when altering the YAML schema or outputs.
- Avoid committing generated artifacts (diagrams, PDFs, tutorials) unless required; keep PRs focused and rebased for a clean history.
- When executing a multi-step plan, complete and commit each step. If no operator input is needed and steps remain, proceed directly to the next step after each commit.

## Branding Notes
- Use the Filare brand in user-facing text, CLI help, docs, and examples; keep legacy `filare` names only where required for compatibility.
- Align naming, colors, and tone with `docs/brand.md`; refresh that file alongside any brand-affecting changes.
