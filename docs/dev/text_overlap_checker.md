# Text Overlap Checker

Detects overlapping text in generated HTML using Playwright/Chromium.

## Usage
- Generate outputs first (examples/tutorials/demos): `uv run --no-sync python src/filare/tools/build_examples.py --output-dir outputs`
- Run checker: `uv run --no-sync filare-check-overlap "outputs/**/*.html" --viewport 1280x720 --warn-threshold 1 --error-threshold 2 --json outputs/overlap-report.json`
- Exit codes: 0 when clean; non-zero if errors. Warnings are reported but do not change exit code unless errors exist.
- Ignore rules (selectors/text regex) via `.filare-overlap-ignore.yml` in repo root; per-page globs supported under `pages:`. CLI flags `--ignore-selector`, `--ignore-text` augment config.
- Thresholds: warn when depth >1px; error when >2px (both configurable).

## CI behavior
- Main CI (`.github/workflows/ci.yml`) runs the checker on pushes to `beta`/`main` after examples are built; it is skipped on PRs.
- Uses the Playwright Python container; no host browser setup needed in CI.

## Docker
- `docker/overlap-check.Dockerfile` builds a Playwright-ready image with `filare-check-overlap` installed via `uv`.
- Example: `docker build -f docker/overlap-check.Dockerfile -t filare-overlap .` then `docker run --rm -v "$PWD:/workspace" filare-overlap "outputs/**/*.html"`.

## Ignoring known cases
Place `.filare-overlap-ignore.yml` in repo root:
```
selectors:
  - ".legend"
text_patterns:
  - "^Draft$"
pages:
  "outputs/examples/*":  # glob on file path
    selectors: [".watermark"]
    text_patterns: ["^Sample$"]
```
CLI flags override/add to these lists when running locally.
