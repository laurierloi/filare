from: docs/research/performance-tools.md

# Perf CI Workflow (On-Demand Profiling)

## Status

PROPOSED

## Priority

Medium

## Summary

Add an opt-in CI workflow that runs profiling scenarios on demand (PR comment/label, beta, or master) to detect adverse performance changes. The workflow uses the perf-tools container and `PerformanceSettings` env flags to capture CPU/memory reports across key Filare commands.

## Motivation

- Provide fast feedback when a change might regress render/BOM performance.
- Keep CI lean by running perf checks only when requested.
- Standardize artifacts (flamegraphs, allocation reports) for comparison across branches.

## Affected Users / Fields

- Maintainers and reviewers assessing performance risk in PRs.
- Release managers validating beta/master stability.

## Scope

- New GitHub Actions workflow (or CI job) triggered by:
  - PR label/comment (e.g., `run-perf`).
  - Scheduled or manual dispatch on `beta`/`master`.
  - Commit messages containing `perf` (optional trigger for automated runs).
- Uses perf-tools container to run representative commands:
  - `filare examples/demo01.yml -f hpst -o outputs`
  - Selected tests in `tests/rendering/` or `tests/bom/` with perf flags.
- Publishes artifacts (py-spy SVG, Scalene HTML, Memray bin/HTML, cProfile pstats) per scenario with run label (branch/commit).
- Optional baseline comparison: attach previous run artifacts or summary metrics.

## Out of Scope

- Automatic perf gating; this workflow is informational only.
- Full benchmark suite or microbenchmarks.

## Requirements

- Trigger controls: PR label/comment (`/run-perf`), workflow_dispatch inputs, and scheduled runs on `beta`/`master`.
- Env-driven profiler toggles via `FIL_PERF_*` settings; default to py-spy + Scalene, Memray optional due to artifact size.
- Cache Graphviz/fonts as needed inside container; avoid global caches.
- Store artifacts as CI uploads; provide links in job summary so operators can download/view flamegraphs, HTML reports, and pstats/callgrind files.
- Document usage in `docs/performance/ci-workflow.md` (what triggers, outputs, interpretation).

## Steps

- [ ] Define workflow file to pull perf-tools container, set `UV_CACHE_DIR=.uv-cache`, and run selected Filare commands with profiling enabled.
- [ ] Implement PR comment/label check to gate execution.
- [ ] Add job summary with links to artifacts and basic metrics (runtime, RSS, CPU%).
- [ ] Document trigger and artifact locations in `docs/performance/ci-workflow.md`.

## Progress Log

- PROPOSED — Derived from performance tooling research.

## Validation

- Dry-run on a sample PR with `/run-perf` comment; confirm artifacts and summary appear.
- Execute on `beta` or `master` via manual dispatch to ensure branch compatibility.

## Dependencies / Risks

- CI time and storage when Memray outputs are enabled; may need size limits or retention rules.
- ptrace/perf permissions on runners; ensure container/run options allow py-spy/Scalene.
