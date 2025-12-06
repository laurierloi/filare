# Caching & Incremental Builds

## Summary
Proposes adding deterministic hashing and artifact caching to skip unchanged work across Filare runs (parse/render/bundle). Goal: speed up CI and batch generation by detecting when inputs/options are identical and reusing outputs.

## Use Cases for Filare
- CI pipelines rerunning on the same inputs with minor changes.
- Large batches of diagrams/BOMs where only a subset changes.
- Developer workflows needing fast feedback on incremental edits.

## Technical Evaluation
- Features: Content hashes over inputs (YAML, components, metadata) and options; cache index mapping hashes to outputs; cache-aware pipeline stages; optional remote cache (CI artifact). Invalidation when Graphviz or template versions change.
- Strengths: Reduces redundant renders; faster CI; less disk churn.
- Weaknesses: Complexity in invalidation; risk of stale outputs if hashing misses dependencies.
- Limitations: Some outputs (PDF bundles) may still need recompute; cache management policies required.
- Compatibility with Filare: Fits pipeline/context refactor; can wrap render functions with cache checks.
- Required integrations: Hashing helper, cache store (local dir), metadata about tool versions; CLI flags to enable/disable cache.

## Complexity Score (1–5)
**4** — Requires pipeline hooks, dependency tracking, and careful invalidation rules.

## Maintenance Risk
- Filare-side: Medium; need to maintain hash inputs and invalidation when templates/Graphviz change.
- External: None; optional remote cache introduces artifact retention concerns.
- Ongoing cost: Keeping cache schema/versioning aligned with code changes.

## Industry / Business Usage
- Build systems (Bazel, Pants) and SSGs use content-addressable caches to speed incremental builds.

## Who Uses It & Why It Works for Them
- **Bazel/Pants**: Incremental builds and remote caching reduce CI times dramatically.
- **Webpack/Vite**: Cache transpilation artifacts keyed on inputs/config.

## Feasibility
- Feasible with pipeline/context refactor to add cache checks per stage; harder to bolt onto current implicit flows.

## Required Work
- **REWORK tasks**: Add hashing of inputs/options/templates; define cache key structure; wrap render/bundle stages with cache lookups; version the cache to invalidate on tool changes.
- **FEATURE tasks**: Optional remote cache integration via CI artifacts; CLI flags for cache control (`--cache`, `--no-cache`, `--cache-dir`).
- **DOCUMENTATION tasks**: Explain cache keys, invalidation events, and how to opt in/out; CI guidance for saving/restoring cache.
- **TOOLS tasks**: Cache inspection/cleanup command.
- **COVERAGE tasks**: Tests for cache hits/misses and invalidation scenarios.

## Recommendation
**ADOPT_LATER** — Valuable for performance, but best tackled after pipeline/config cleanup and with clear invalidation rules.

## References
- Content-addressable caching patterns from Bazel/Pants; incremental build caches in SSGs.
