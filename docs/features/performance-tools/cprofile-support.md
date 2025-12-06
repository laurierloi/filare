from: docs/research/performance-tools.md

# cProfile Support (Deterministic CPU Profiling)

## Status

PROPOSED

## Priority

Low

## Summary

Add opt-in cProfile support via env-configured settings (`FIL_PERF_CPROFILE_*`) to produce `pstats`/callgrind outputs for Filare runs, using the perf-tools container for consistent tooling.

## Motivation

- Provide a stdlib, dependency-free profiling option.
- Deterministic call counts useful for regression diffs and small benchmarks.
- Works in constrained environments where py-spy/Scalene are unavailable.

## Affected Users / Fields

- Developers needing deterministic call traces for CLI commands.
- CI jobs capturing quick comparisons of hotspots over time.

## Scope

- Add `CProfileSettings` (prefix `FIL_PERF_CPROFILE_`) nested in `PerformanceSettings`.
- Options: sort key (time/calls), output format (`pstats`, `callgrind`), strip dirs toggle, subcommand to wrap.
- Wrapper in perf container to run `python -m cProfile` with configured options, writing `run_label-cprofile.*`.
- Documentation page `docs/performance/cprofile.md` describing running, converting to callgrind, and viewing with `snakeviz`/`kcachegrind`.

## Out of Scope

- Runtime UI integration; outputs remain files for offline analysis.

## Requirements

- Env vars such as `FIL_PERF_CPROFILE_ENABLED`, `FIL_PERF_CPROFILE_SORT=time`, `FIL_PERF_CPROFILE_FORMAT=pstats|callgrind`, `FIL_PERF_CPROFILE_OUTPUT`.
- Default output path under `PerformanceSettings.output_dir` with `run_label`.
- Support generating callgrind via `pyprof2calltree` inside the container when requested.
- Docs page with examples and report interpretation tips, including:
  - How to view `pstats` summaries (top functions by `tottime`/`cumtime`).
  - Opening `callgrind` in `kcachegrind` or `qcachegrind` for call graph visualization.
  - Using `snakeviz` for interactive browser-based views (optional in perf-tools container).

## Steps

- [ ] Define `CProfileSettings` model with defaults (sort `tottime`, format `pstats`).
- [ ] Wire settings to container wrapper and `PerformanceSettings.enable_cprofile`.
- [ ] Add optional conversion step to callgrind if requested.
- [ ] Document usage in `docs/performance/cprofile.md`.

## Progress Log

- PROPOSED — Based on performance-tooling research.

## Validation

- Run `FIL_PERF_CPROFILE_ENABLED=1` on sample Filare command; confirm output file and readable stats.
- Verify callgrind conversion opens in `kcachegrind` if requested.

## Dependencies / Risks

- Overhead higher than sampling tools; keep for targeted measurements.
- Callgrind conversion requires extra tool (`pyprof2calltree`) in the perf container.
