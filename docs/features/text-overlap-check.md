# Text Overlap Check for Generated HTML
uid: FEAT-DOCS-0004
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Goal

Add a tooling-only check that fails when rendered text in generated HTML overlaps visually. This guards regressions where labels or annotations collide after layout changes.

## Requirements

- Input: path(s) to generated HTML (single file or directory glob); default to all generated pages (docs + examples/outputs).
- Rendering: use a headless browser to evaluate final layout (fonts, CSS, SVG/Canvas) at a configurable viewport size; default to the docs/CI viewport (e.g., 1280x720).
- Detection: identify bounding boxes for visible text and flag overlapping rectangles; ignore hidden/zero-size elements and non-text nodes.
- Output: machine-readable report (JSON) listing offending elements (text snippet, selectors/xpaths, bounding boxes, page URL) plus a human summary with counts.
- Exit codes: 0 when no overlap; non-zero when overlaps detected or on fatal errors. Support two severity thresholds: warning when intersection depth is >0 and <=2 px; error when >2 px. Thresholds must be configurable.
- CI ready: runnable via `uv run` without network; Chromium/Playwright install handled by tooling or documented pre-req.
- Config: allow ignore lists (selectors/regex), viewport overrides, and per-page thresholds (e.g., max N overlaps before fail). Desktop-only viewport is sufficient for initial implementation.
- Performance: able to check the current docs/examples set within CI time budgets; parallelize pages when possible.

## Proposed Approach

1. Use Playwright (Python) to load each HTML with a fixed viewport. Evaluate in-page JS to:
   - Collect all visible text nodes and their bounding boxes (e.g., elements with non-empty `innerText`, display != none, visibility != hidden, opacity > 0, non-zero rect).
   - Compute pairwise rectangle intersections; record pairs that overlap more than a small epsilon.
   - Return structured data (node locator hint, text snippet, rect).
2. CLI entrypoint (tooling-only) under `src/filare/tools/`:
   - Example: `uv run filare-check-overlap outputs/examples/**/*.html --viewport 1280x720 --ignore ".legend, .tooltip" --max-overlaps 0`.
   - Emit JSON to stdout and a brief summary line; support `--json path` to write the report.
3. Integration:
   - Add a CI job on `beta`/`main` pushes (skip PRs) so it runs after examples/docs are built; keep runtime manageable (e.g., allow opt-in via workflow input/matrix).
   - Provide a Docker image (or `Dockerfile`) with Playwright/Chromium and required fonts so CI/local runs are consistent and do not depend on host setup; optionally wrap via `scripts/check-overlap.sh`.
   - Use glob-based page matching for ignores; config file lives at repo root as `.filare-overlap-ignore.yml`.

## Ignore Mechanism

- Support both selector-based and text-regex ignores.
- Provide a project-level config file (e.g., `.filare-overlap-ignore.yml`) with entries like:
  ```
  selectors:
    - ".legend"
    - ".tooltip"
  text_patterns:
    - "^Page \\d+$"
  pages:
    "docs/examples/*":  # glob for page URL/path
      selectors: [".watermark"]
      text_patterns: ["^Draft$"]
  ```
- CLI flags override/augment config (e.g., `--ignore-selector ".legend"` or `--ignore-text "Draft"`).
- Ignore logic should drop any overlap pair if either node matches an ignore rule.

## Open Questions / Decisions Needed

- Confirm whether any additional ignore file defaults are needed beyond `.filare-overlap-ignore.yml`.
- Confirm whether page-scoped ignores should support advanced glob features (current plan: glob).
- Decide whether to add a follow-up feature to manage ignore baselines (e.g., auto-suggest ignores when overlaps are deemed acceptable).
- Which pages to check by default (all generated examples, docs, specific outputs)?
- Should small overlaps (e.g., 1–2 px touch) be tolerated via a threshold?
- Do we need per-viewport checks (desktop + mobile), or is desktop-only sufficient initially?
- Preferred ignore mechanism (selectors vs. text regex) and how to store project-wide ignores (config file vs. CLI flags).
