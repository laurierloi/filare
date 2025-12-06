from: docs/research/performance-tools.md

# Scalene Support (CPU + Memory Sampling)

## Status

PROPOSED

## Priority

Medium (upgrade to High if memory regressions become frequent)

## Summary

Expose Scalene as an opt-in profiler via env-driven settings (`FIL_PERF_SCALENE_*`) and containerized tooling to capture line-level CPU, memory, and copy costs during Filare runs.

## Motivation

- Identify mixed CPU/memory bottlenecks in parsing and rendering paths.
- Detect allocation-heavy lines and potential leaks.
- Provide richer diagnostics than CPU-only sampling.

## Affected Users / Fields

- Developers chasing memory spikes or slowdowns in large diagram/BOM builds.
- CI maintainers needing one-off allocation reports on regressions.

## Scope

- Add `ScaleneSettings` (prefix `FIL_PERF_SCALENE_`) nested in `PerformanceSettings`.
- Flags for CPU sampling rate, memory profiling toggle, copy-cost tracking, and output format (text vs. HTML).
- Wrapper in perf container to run `scalene` with configured options, writing reports to `output_dir/run_label-scalene.*`.
- Documentation page `docs/performance/scalene.md` describing usage and interpreting CPU/memory columns.

## Out of Scope

- Permanent instrumentation inside Filare code.
- Support for Windows (container target is Linux).

## Requirements

- Env vars such as `FIL_PERF_SCALENE_ENABLED`, `FIL_PERF_SCALENE_CPU_RATE`, `FIL_PERF_SCALENE_MEMORY=1`, `FIL_PERF_SCALENE_HTML=1`.
- Respect `PerformanceSettings.output_dir` and `run_label` for file naming.
- Clear warnings about overhead and noise on very short runs.
- Docs page with example commands and sample report snippets.
- Platform check: supported primarily on Linux (container target); skip or warn in CI/dev when unavailable.

## Steps

- [ ] Define `ScaleneSettings` model with defaults (CPU sampling 0.01s, memory on, HTML off by default).
- [ ] Wire settings to container wrapper command and `PerformanceSettings.enable_scalene`.
- [ ] Add helper to choose output filename/format based on settings.
- [ ] Document usage in `docs/performance/scalene.md` with screenshots or snippets.

## Progress Log

- PROPOSED — Based on performance-tooling research.

## Validation

- Run `FIL_PERF_SCALENE_ENABLED=1` on a representative Filare build; verify output files and that CPU/memory attribution shows expected hotspots.
- Measure overhead vs. baseline to ensure tolerable performance.

## Dependencies / Risks

- Higher overhead than py-spy; advise use on reproducible runs only.
- May require `LD_PRELOAD` tweaks in some environments; document if needed.
