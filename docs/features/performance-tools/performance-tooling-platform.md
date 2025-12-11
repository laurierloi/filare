from: docs/research/performance-tools.md

uid: FEAT-PERF-0004
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Performance Tooling Platform (Container + Settings)

## Status

PROPOSED

## Priority

High

## Summary

Ship a dedicated Docker image that bundles py-spy, Scalene, Memray, and cProfile utilities, and introduce Pydantic-based performance settings (`FIL_PERF_` prefix) to toggle and configure profilers via environment variables across Filare CLIs and harness tools.

## Motivation

- Provide a reproducible profiling environment without polluting developer machines.
- Enable opt-in profiling in CI/local runs using only environment flags, avoiding CLI changes per tool.
- Standardize output locations and formats for generated flamegraphs and reports.

## Affected Users / Fields

- Developers diagnosing slow renders or memory spikes.
- CI maintainers capturing performance snapshots on regressions.
- Downstream harness users needing repeatable profiling runs.

## Scope

- Build/publish a `filare/perf-tools` container with py-spy, Scalene, Memray, Graphviz deps, and helper scripts.
- Add `PerformanceSettings` Pydantic model (prefix `FIL_PERF_`) with per-tool enable flags and shared options (output dir, run label, container image tag).
- Wire settings into CLI entrypoints and harness scripts so profiling is activated based on env vars.
- Document usage under `docs/performance/` with tool-specific guides and expected report artifacts.
- Support volume mounts for:
  - Output persistence (e.g., `-v $PWD/outputs/perf:/workspace/outputs/perf`).
  - Using local Filare source as the package inside the container for iterative dev/CI (`-v $PWD:/workspace/filare` with editable install).

## Out of Scope

- Core algorithm rewrites or optimizations.
- Always-on profiling in production; features remain opt-in.
- Non-Linux containers.

## Requirements

- `PerformanceSettings` fields (prefix `FIL_PERF_`):
  - `enable_pyspy`, `enable_scalene`, `enable_memray`, `enable_cprofile` (bools).
  - `output_dir` (default `outputs/perf`), `run_label` (for filenames), `container_image` (default perf image tag).
- Volume usage must be documented:
  - Host output dir to container `output_dir`.
  - Bind local Filare repo for editable installs during development and for CI reproducibility.
- Per-tool nested settings classes with prefixes:
  - `FIL_PERF_SPY_*` (py-spy), `FIL_PERF_SCALENE_*` (Scalene), `FIL_PERF_MEMRAY_*` (Memray), `FIL_PERF_CPROFILE_*` (cProfile).
- Helper scripts inside the container to run `filare` with selected profiler and emit flamegraphs/callgrind/memory reports.
- CI-friendly defaults: disabled unless enable flag is set; errors on missing permissions reported clearly.
- Docs to create: `docs/performance/overview.md` describing settings, env prefixes, container invocation, and output formats.

## Steps

- [ ] Define Pydantic `PerformanceSettings` with enable flags and shared options; register in CLI config path.
- [ ] Define nested tool settings models with prefixes (`FIL_PERF_SPY`, `FIL_PERF_SCALENE`, `FIL_PERF_MEMRAY`, `FIL_PERF_CPROFILE`) and defaults.
- [ ] Add helper wrappers (e.g., `scripts/perf/py-spy.sh`, `scripts/perf/scalene.sh`, etc.) that honor settings and write to `output_dir/run_label-*`.
- [ ] Build `filare/perf-tools` Dockerfile including profilers + Graphviz; publish image/tag.
- [ ] Document workflows in `docs/performance/overview.md` and link tool-specific pages.

## Progress Log

- PROPOSED — Derived from performance-tools research.

## Validation

- Run `uv run filare ...` inside the perf container with each profiler enabled via env; verify outputs written to configured dir with run label.
- Confirm settings parsing from env works without code changes to CLI args.
- Smoke-test on CI runner for permission/ptrace issues.

## Dependencies / Risks

- Container size and build time may grow with multiple profilers.
- ptrace/perf_event permissions may block py-spy/perf on hardened hosts; documentation needed.
- Need to keep tool versions in sync with supported Python versions.
