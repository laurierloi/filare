# Performance Analysis Tooling

## Summary

Survey of Python-friendly performance and observability tools that can profile Filare’s CLI/library runtime across CPU, memory, and lock/GIL contention. Focus is on low-integration options that work with `uv run filare ...` and can attach to existing processes without changing Filare code.

## Use Cases for Filare

- Diagnose slow renders in `filare`/`filare-qty` runs (Graphviz/HTML/BOM generation).
- Track CPU hotspots when parsing large YAML inputs or heavy component metadata.
- Detect memory leaks or excessive allocations during batch diagram builds.
- Measure GIL/lock contention when using threads/subprocesses for rendering.
- Capture process-level resource envelopes to size CI runners and downstream harness machines.

## Technical Evaluation

- **cProfile + pstats (stdlib)**
  - Features: Deterministic function-level CPU profiling; ships with Python.
  - Strengths: Zero dependencies; stable API; integrates with existing test runs.
  - Weaknesses: Higher overhead; no memory insight; noisy for short-lived functions.
  - Limitations: Cannot attach to running processes; output requires manual formatting.
  - Compatibility with Filare: Wrap `uv run filare ...` to profile CLI entrypoints; works in CI for regressions.
  - Required integrations: Optional helper script to run `cProfile` and emit `pstats`/callgrind files.
- **py-spy**
  - Features: Sampling profiler that can attach to live Python processes; thread-aware; shows time waiting on the GIL.
  - Strengths: Low overhead; no code changes; safe to use on production-like runs; exports flamegraphs.
  - Weaknesses: Limited memory visibility; sampling can miss very short functions.
  - Limitations: Requires `ptrace` permission; primarily CPU/GIL focused.
  - Compatibility with Filare: Can attach to `uv run filare ...` or record a run to SVG; helpful for lock/GIL hotspots when rendering diagrams.
  - Required integrations: Add doc snippets for `UV_CACHE_DIR=.uv-cache uv run py-spy record -- output.svg -- uv run filare ...`.
- **Scalene**
  - Features: Line-level CPU and memory sampling with GIL attribution and copy cost detection.
  - Strengths: Highlights CPU vs. memory-heavy lines; detects leaks; works with threads.
  - Weaknesses: Higher overhead than py-spy; reports are more complex to interpret.
  - Limitations: Not ideal for very short runs; requires Python 3.8+.
  - Compatibility with Filare: Run `UV_CACHE_DIR=.uv-cache uv run scalene --cpu --memory --filare ...` to spot heavy parsing/rendering paths.
  - Required integrations: Document invocation examples and add ignore patterns for profiler outputs if needed.
- **Memray**
  - Features: Comprehensive memory allocator tracer (Python + native) with flamegraphs and leak views.
  - Strengths: Captures allocations across Python/C extensions (Graphviz); good for peak memory tracking.
  - Weaknesses: Higher runtime overhead; generates large reports.
  - Limitations: Best for repro runs, not continuous CI; Linux/macOS only.
  - Compatibility with Filare: Wrap CLI runs to find leaks during large diagram builds; useful when BOM generation spikes memory.
  - Required integrations: Provide optional `uv run memray run -o run.bin -- filare ...` instructions and viewer steps.
- **Linux perf (perf stat/record + FlameGraph)**
  - Features: System-level sampling of CPU, context switches, and locks (with `perf lock`); captures native stacks.
  - Strengths: Very low overhead; observes Python + native (Graphviz, libc); shows scheduler/lock behavior.
  - Weaknesses: Linux-only; requires permissions (`perf_event_paranoid`); output needs post-processing.
  - Limitations: Less Python-specific; symbol resolution for Python frames requires `perf map` support.
  - Compatibility with Filare: Useful for render-heavy workloads where native Graphviz dominates; can reveal context-switch storms.
  - Required integrations: Document `perf stat -d -- uv run filare ...` and optional `perf script` + `FlameGraph` steps; avoid CI unless perf is available.

## Complexity Score (1–5)

**2** — Tooling can be added as optional developer workflows without altering Filare’s code. Integration is limited to docs/scripts; the main effort is curating example commands and ignoring generated profiler artifacts.

## Maintenance Risk

- py-spy, Scalene, and Memray are active OSS projects with regular releases; stdlib cProfile is stable; Linux perf is maintained with the kernel.
- Risks: Kernel/ptrace permissions can block py-spy/perf on hardened hosts; Memray/Scalene may need periodic pinning for Python version bumps.
- Filare-side work: Maintain docs and optional helper scripts; ensure `UV_CACHE_DIR` use when adding profiling commands.
- External reliability: Low; tools are mature, but binary wheels may lag behind new Python versions temporarily.

## Industry / Business Usage

- Profiling tooling is standard in enterprise Python stacks for services and CLI utilities; low-overhead sampling is preferred for production-like runs.
- Memray was open-sourced by Bloomberg to diagnose allocator-heavy workloads (e.g., market data pipelines) and targets mixed Python/C stacks.
- Linux perf is widely used by systems teams for CPU/lock tuning and is relied on by CPython core developers when optimizing interpreter hotspots.
- py-spy and Scalene are common in PyData/ML communities for notebook and batch job tuning where attaching to a live process is important.

## Who Uses It & Why It Works for Them

- **Bloomberg (Memray)**: Created Memray to trace Python and native allocations in production services; allocation flamegraphs reduced time-to-fix for leaks and peak RSS spikes.
- **CPython core developers (Linux perf/pyperf)**: Use perf sampling to spot interpreter bottlenecks and native regressions with minimal overhead on large benchmarks.
- **Ben Frederickson / RecSys blog (py-spy)**: Uses py-spy to attach to running recommendation service experiments, capturing flamegraphs without restarting processes.
- **University teaching/research labs (Scalene)**: Adopt Scalene for coursework and experiments to illustrate CPU vs. memory bottlenecks with line-level granularity.

## Feasibility

- Feasible now as optional tooling and documentation.
- No REWORK or FEATURE blockers; only optional helper scripts and doc additions are needed.

## Required Work

- **REWORK tasks**: None unless we later add profiling hooks into the CLI.
- **FEATURE tasks**: Optional `filare --profile` wrapper or `scripts/profile_filare.sh` to standardize cProfile/py-spy runs.
- **DOCUMENTATION tasks**: Add a developer doc page describing profiling recipes (py-spy, Scalene, Memray, perf) and example commands using `uv run`.
- **TOOLS tasks**: Provide ignore patterns for profiler artifacts; optionally vendor FlameGraph scripts or a Make target for perf/py-spy captures.
- **COVERAGE tasks**: Not applicable; profiling is observational.

## Recommendation

**ADOPT** — Standardize on py-spy (CPU/GIL), Scalene (CPU+memory), Memray (allocation tracing), and cProfile (baseline) as optional developer tools; document Linux perf for native hot paths.

## References

- py-spy: https://github.com/benfred/py-spy
- Scalene: https://github.com/plasma-umass/scalene
- Memray: https://github.com/bloomberg/memray
- cProfile/pstats: https://docs.python.org/3/library/profile.html
- Linux perf + FlameGraph: https://perf.wiki.kernel.org and https://github.com/brendangregg/FlameGraph

## Optional Appendix

- Example commands:
  - CPU/GIL flamegraph: `UV_CACHE_DIR=.uv-cache uv run py-spy record -o filare.svg -- uv run filare examples/demo01.yml -f hpst -o outputs`
  - Line-level CPU/memory: `UV_CACHE_DIR=.uv-cache uv run scalene --cpu --memory -- filare examples/demo01.yml -f hpst -o outputs`
  - Allocation tracing: `UV_CACHE_DIR=.uv-cache uv run memray run -o filare.bin -- filare examples/demo01.yml -f hpst -o outputs`
  - System-level stats: `perf stat -d -- uv run filare examples/demo01.yml -f hpst -o outputs`
