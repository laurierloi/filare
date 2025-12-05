# Text Overlap Check for Generated HTML

## Goal
Add a tooling-only check that fails when rendered text in generated HTML overlaps visually. This guards regressions where labels or annotations collide after layout changes.

## Requirements
- Input: path(s) to generated HTML (single file or directory glob).
- Rendering: use a headless browser to evaluate final layout (fonts, CSS, SVG/Canvas) at a configurable viewport size; default to the docs/CI viewport (e.g., 1280x720).
- Detection: identify bounding boxes for visible text and flag overlapping rectangles; ignore hidden/zero-size elements and non-text nodes.
- Output: machine-readable report (JSON) listing offending elements (text snippet, selectors/xpaths, bounding boxes, page URL) plus a human summary with counts.
- Exit codes: 0 when no overlap; non-zero when overlaps detected or on fatal errors.
- CI ready: runnable via `uv run` without network; Chromium/Playwright install handled by tooling or documented pre-req.
- Config: allow ignore lists (selectors/regex), viewport overrides, and per-page thresholds (e.g., max N overlaps before fail).
- Performance: able to check the current docs/examples set within CI time budgets; parallelize pages when possible.

## Proposed Approach
1) Use Playwright (Python) to load each HTML with a fixed viewport. Evaluate in-page JS to:
   - Collect all visible text nodes and their bounding boxes (e.g., elements with non-empty `innerText`, display != none, visibility != hidden, opacity > 0, non-zero rect).
   - Compute pairwise rectangle intersections; record pairs that overlap more than a small epsilon.
   - Return structured data (node locator hint, text snippet, rect).
2) CLI entrypoint (tooling-only) under `src/filare/tools/`:
   - Example: `uv run filare-check-overlap outputs/examples/**/*.html --viewport 1280x720 --ignore ".legend, .tooltip" --max-overlaps 0`.
   - Emit JSON to stdout and a brief summary line; support `--json path` to write the report.
3) Integration:
   - Add an optional CI job (beta PR workflow) gated by a flag or matrix entry to keep runtime manageable.
   - Document prerequisites (Playwright `install` step) in `docs/ci.md` and `scripts/check-overlap.sh` wrapper.

## Open Questions / Decisions Needed
- Which pages to check by default (all generated examples, docs, specific outputs)?
- Should small overlaps (e.g., 1–2 px touch) be tolerated via a threshold?
- Do we need per-viewport checks (desktop + mobile), or is desktop-only sufficient initially?
- Preferred ignore mechanism (selectors vs. text regex) and how to store project-wide ignores (config file vs. CLI flags).
