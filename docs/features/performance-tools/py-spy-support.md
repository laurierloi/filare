from: docs/research/performance-tools.md

# py-spy Support (Sampling CPU/GIL)

## Status

PROPOSED

## Priority

Medium

## Summary

Integrate py-spy as an opt-in sampling profiler for Filare CLIs, configured via Pydantic settings (`FIL_PERF_SPY_*`) and runnable inside the shared perf-tools container to generate flamegraphs and GIL contention views.

## Motivation

- Low-overhead CPU profiling without code changes.
- Ability to attach or wrap `filare` runs to visualize hotspots and GIL wait time.
- Works well for render-heavy workloads and CI snapshots.

## Affected Users / Fields

- Developers diagnosing slow diagram rendering or parser hotspots.
- CI operators capturing flamegraphs on suspected regressions.

## Scope

- Add `PySpySettings` (prefix `FIL_PERF_SPY_`) nested under `PerformanceSettings`.
- Support flags: sampling rate (Hz), output format (`svg`/`raw`), whether to record or live top, target PID vs. wrap mode, native symbols toggle, blocklist for threads.
- Wrapper script in perf container to run `py-spy record` with settings and emit `run_label-pyspy.svg`.
- Documentation page `docs/performance/py-spy.md` describing usage, required permissions, and sample outputs.
- Platform awareness: primary support on Linux (container target); surface clear messaging/skip logic on unsupported platforms or when ptrace is blocked.

## Out of Scope

- Persistent agent for long-lived services.
- Non-Linux support beyond containerized runs.

## Requirements

- Env-configurable via `FIL_PERF_SPY_` (e.g., `FIL_PERF_SPY_ENABLED`, `FIL_PERF_SPY_RATE`, `FIL_PERF_SPY_OUTPUT=svg`, `FIL_PERF_SPY_NATIVE=1`, `FIL_PERF_SPY_PID`).
- Honor global `PerformanceSettings.output_dir` and `run_label` for output naming.
- Graceful error when ptrace is blocked; log hint to enable `SYS_PTRACE` in Docker or adjust `kernel.yama.ptrace_scope`.
- Docs page to include command examples (wrap and attach) and how to read flamegraph.
- CI/dev runs must check host platform and ptrace capability; skip or warn when unsupported rather than failing tests.

## Steps

- [ ] Define `PySpySettings` model with default rate (100 Hz), output `svg`, native disabled by default.
- [ ] Wire settings to wrapper script (wrap or attach) and integrate with `PerformanceSettings.enable_pyspy`.
- [ ] Add container entrypoint alias for py-spy runs (e.g., `perf-pyspy filare ...`).
- [ ] Write `docs/performance/py-spy.md` with env examples and report interpretation.

## Progress Log

- PROPOSED — Based on performance-tooling research.

## Validation

- Run wrapped `uv run filare ...` in container with `FIL_PERF_SPY_ENABLED=1`; confirm SVG generated in `output_dir`.
- Attach mode test against a long-running filare process.
- Verify GIL visualization is present when `--native` enabled.

## Dependencies / Risks

- Requires ptrace permission in container/host.
- Sampling may miss very short functions; note in docs.
