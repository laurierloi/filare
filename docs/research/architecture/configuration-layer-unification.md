# Configuration Layer Unification

## Summary

Recommend consolidating Filare configuration into layered Pydantic settings under `src/filare/config/` with clear prefixes and sources (env → CLI args → file), replacing scattered ad-hoc dicts and minimal `FilareSettings`. All configuration should merge into a single resolved representation (single source of truth) that downstream steps consume.

## Use Cases for Filare

- Consistent handling of Graphviz engine, output directories, feature toggles (e.g., performance profiling, experimental diagrams) across CLI, tests, and downstream harnesses.
- Easier CI overrides via env vars without editing YAML inputs.
- Shared settings structure for future API/server usage.
- Centralized config models and loader in `src/filare/config/`, emitting a single resolved configuration object used across flows.

## Technical Evaluation

- Features: Central `Settings` module with nested models (render, parsing, performance, paths), a resolver for precedence (env → CLI → file), and typed defaults. Provide helpers to load settings once and inject into flows, yielding a single resolved config instance.
- Strengths: Eliminates implicit coupling between CLI options and in-code defaults; reduces drift across commands and scripts; improves validation and discoverability; single source of truth simplifies staged processing.
- Weaknesses: Requires migrating option parsing to use the settings layer; risk of mismatch during transition.
- Limitations: Needs careful mapping to avoid breaking existing CLI flags or YAML schema.
- Compatibility with Filare: Pydantic already used; can expand `settings.py` (or new `config/` package) and adapt CLI/flows incrementally.
- Required integrations: CLI should hydrate settings and pass them into `parse`/flows; docs to explain prefixes (e.g., `FIL_`, `FIL_PERF_`, `FIL_RENDER_`).

## Complexity Score (1–5)

**3** — Moderate: defining models and migrating option wiring; minimal algorithmic risk.

## Maintenance Risk

- Filare-side: Medium during migration; long-term reduction by making config explicit and validated.
- External: None; Pydantic is stable and already a dependency.
- Ongoing cost: Low; new options follow a consistent pattern.

## Industry / Business Usage

- Many CLIs (Terraform, uv, Docker) employ layered config (env + flags + files) with explicit precedence for reproducibility and CI friendliness.
- Python services commonly use Pydantic settings to centralize env parsing and validation.

## Who Uses It & Why It Works for Them

- **FastAPI-based services**: Rely on Pydantic settings for env/secret handling with clear precedence.
- **Terraform/Docker CLIs**: Use env/flag layering so automation can override defaults without patching config files.

## Feasibility

- Feasible now; aligns with existing Pydantic usage and pending performance settings work.

## Required Work

- **REWORK tasks**: Expand `settings.py` into layered models (render, paths, performance, experimental flags) within `src/filare/config/`; define precedence resolver producing a single resolved config object; replace mutable `extra_metadata` patterns with typed config injection.
- **FEATURE tasks**: Add config file ingestion (e.g., `.filare.toml/yaml`) as an optional source; expose settings dump for debugging.
- **DOCUMENTATION tasks**: Document prefixes, precedence, and mapping from CLI flags to settings; add examples for CI/local usage.
- **TOOLS tasks**: Add a `filare settings show` or debug flag to print resolved settings.
- **COVERAGE tasks**: Tests for precedence, validation errors, and backward compatibility of defaults.

## Recommendation

**ADOPT** — Prioritize configuration unification to reduce drift and prepare for additional toggles (performance, experimental diagrams, cache control).

## References

- Pydantic BaseSettings patterns; layered config precedence used by common CLIs.

## Optional Appendix

- Draft prefixes: `FIL_RENDER_*`, `FIL_PATH_*`, `FIL_PERF_*`, `FIL_EXPERIMENTAL_*`; file-based override example `.filare.yml`.
