from: docs/research/performance-tools.md

uid: FEAT-PERF-0002
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# Memray Support (Allocation Tracing)

## Status

PROPOSED

## Priority

Medium (elevate to High when investigating memory regressions)

## Summary

Integrate Memray as an opt-in allocation tracer controlled via env (`FIL_PERF_MEMRAY_*`) and runnable from the perf-tools container to capture Python/native allocations, leaks, and peak RSS during Filare runs.

## Motivation

- Track down memory leaks or spikes when rendering complex diagrams or large BOMs.
- Observe allocations in native extensions (e.g., Graphviz) as well as Python code.
- Provide exportable flamegraphs and table reports for investigations.

## Affected Users / Fields

- Developers debugging memory issues in Filare or downstream harnesses.
- CI snapshots when memory usage regresses between releases.

## Scope

- Add `MemraySettings` (prefix `FIL_PERF_MEMRAY_`) nested in `PerformanceSettings`.
- Flags for output file, format (bin/HTML/flamegraph), track allocations vs. deallocations, native frame collection, and live server toggle.
- Container wrapper to run `memray run` with configured options and emit `run_label-memray.*`.
- Documentation page `docs/performance/memray.md` describing capture, viewing (`memray flamegraph/summary/html`), and expected artifacts.

## Out of Scope

- Always-on memory tracing; intended for targeted repros.
- Windows support (container base is Linux).

## Requirements

- Env vars such as `FIL_PERF_MEMRAY_ENABLED`, `FIL_PERF_MEMRAY_OUTPUT`, `FIL_PERF_MEMRAY_FORMAT=html|flamegraph|bin`, `FIL_PERF_MEMRAY_NATIVE=1`, `FIL_PERF_MEMRAY_LIVE_PORT`.
- Default output path under `PerformanceSettings.output_dir` with `run_label`.
- Graceful handling of large report sizes; warn when live server is enabled.
- Docs page with command examples and viewing instructions.
- Platform note: target Linux container; skip/warn on unsupported platforms in CI/dev.

## Steps

- [ ] Define `MemraySettings` model with sensible defaults (binary output, native frames off, live server off).
- [ ] Wire settings to container wrapper and `PerformanceSettings.enable_memray`.
- [ ] Provide helper to convert captured `.bin` into flamegraph/HTML when requested.
- [ ] Document usage in `docs/performance/memray.md`.

## Progress Log

- PROPOSED — Based on performance-tooling research.

## Validation

- Run with `FIL_PERF_MEMRAY_ENABLED=1` on a heavy Filare example; ensure output file exists and can be rendered via `memray flamegraph`/`memray summary`.
- Confirm native frames appear when enabled.

## Dependencies / Risks

- Overhead higher than sampling profilers; limit to repro runs.
- Report files can be large; note cleanup practices.
