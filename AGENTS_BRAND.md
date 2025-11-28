# Repository Guidelines (Filare)

## Project Structure & Module Organization
- Core library and CLI live in `src/wireviz/`; `wv_cli.py` exposes the `filare`/`filare-qty` commands (legacy `wireviz`/`wireviz-qty` remain for compatibility), with rendering and BOM logic in `wv_graphviz.py`, `wv_output.py`, and helpers under `tools/`.
- Documentation is under `docs/` (see `docs/README.md` and `docs/syntax.md`), with walkthroughs in `tutorial/` and ready-made YAML inputs in `examples/`.
- Architecture/data-flow/model diagrams live in `docs/graphs/`; update the Mermaid sources and regenerate rendered outputs when code structure changes.
- Regression YAMLs live in `tests/rendering/` and `tests/bom/`; write generated outputs to `outputs/` or a temp directory.
- Harness definitions for XSC live next door in `../xsc-harnesses`; treat them as downstream consumers built with the same Filare virtualenv.

## Build, Test, and Development Commands
- Prefer uv for env and installs:
  - Create venv: `UV_CACHE_DIR=./.uv-cache uv venv .venv`
  - Install (incl. dev tools): `UV_CACHE_DIR=./.uv-cache uv pip install --python .venv/bin/python -e . --group dev`
  - Run tests/coverage: `UV_CACHE_DIR=./.uv-cache uv run --python .venv/bin/python pytest`
- Quick sanity run: `UV_CACHE_DIR=./.uv-cache uv run --python .venv/bin/python filare examples/demo01.yml -f hpst -o outputs` (HTML/PNG/SVG/TSV). Add `-c examples/components.yml` or `-d metadata.yml` as needed.
- Build downstream harnesses with the same venv: `cd ../xsc-harnesses && FILARE=../WireViz-codex1/.venv/bin/filare make` (use `WIREVIZ=` if the harness makefile still expects the legacy variable); `make clean` removes generated SVG/PNG/PDF/TSV.
- For manual BOM scaling checks: `UV_CACHE_DIR=./.uv-cache uv run --python .venv/bin/python filare-qty tests/bom/bomqty.yml --use-qty-multipliers`.

## Coding Style & Naming Conventions
- Python 3.8+; 4-space indentation; follow existing naming (`wv_*` modules, lowercase functions).
- Format with Black and organize imports with isort. Run `./cleanup.sh` to apply autoflake + isort + black across `src/wireviz/`.
- Docstrings follow Google style; keep CLI help strings succinct and user-facing.
- Template and asset names stay lowercase with hyphens or underscores; keep YAML keys lowercase.
- Keep docs coherent with code: when modifying metadata, flows, parser, or render behavior, update `docs/`, `docs/dev/`, and `docs/graphs/` accordingly (metadata guides, syntax, diagrams).

## Testing Guidelines
- No full automated test harness is wired up; use YAMLs in `tests/` and `examples/` to spot rendering/BOM regressions.
- Add a minimal YAML in `tests/rendering/` or `tests/bom/` for new behavior; keep file names numeric-prefixed (`04_newfeature.yml`).
- Also build the XSC harness suite with the project venv (`cd ../xsc-harnesses && FILARE=../WireViz-codex1/venv-wireviz/bin/filare make`, or `WIREVIZ=` for legacy makefiles) to catch downstream breakage.
- Ensure GraphViz (`dot -V`) and required fonts are available before debugging rendering differences.

## Commit & Pull Request Guidelines
- Open an issue first, then branch from `dev`. Use imperative, concise commit subjects and reference the issue number in the body when applicable.
- Base PRs on `dev`; describe the user-visible change, mention new YAML examples/tests (including any XSC harness updates), and link related issues. Update `docs/syntax.md` when altering the YAML schema or outputs.
- Avoid committing generated artifacts (diagrams, PDFs, tutorials) unless required; keep PRs focused and rebased for a clean history.
- When executing a multi-step plan, complete and commit each step. If no operator input is needed and steps remain, proceed directly to the next step after each commit.

## Branding Notes
- Use the Filare brand in user-facing text, CLI help, docs, and examples; keep legacy `wireviz` names only where required for compatibility.
- Align naming, colors, and tone with `docs/brand.md`; refresh that file alongside any brand-affecting changes.
