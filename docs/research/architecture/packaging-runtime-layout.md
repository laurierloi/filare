# Packaging & Runtime Layout Simplification

## Summary

Suggest clarifying the separation between CLI-facing code and core library modules by organizing runtime layout (e.g., `filare.cli.*` vs `filare.core.*`) and reducing cross-module coupling. Aim to make embedding/API usage clearer and ease future serverization while keeping CLI behavior stable.

## Use Cases for Filare

- Developers embedding Filare as a library without pulling CLI concerns.
- Future API/server exposure with a clean core surface area.
- Clearer dependency boundaries for flows/renderers vs. CLI/IO.

## Technical Evaluation

- Features: Introduce a clearer package layout (e.g., `filare/core/` for models/flows/render, `filare/cli/` for entrypoints/settings), with thin adapters between CLI/config and core orchestrator. Minimize side effects at import time.
- Strengths: Improves readability and maintainability; makes public API surfaces explicit; simplifies dependency management and testing.
- Weaknesses: Requires moving modules and updating imports; migration risk if paths change without shims.
- Limitations: Need to preserve existing entrypoints (`filare`, `filare-qty`) and backward-compatible imports.
- Compatibility with Filare: Aligns with proposed pipeline/config refactors; can be phased with deprecation shims for import paths.
- Required integrations: Module reorg, import shims, documentation of public API surface.

## Complexity Score (1–5)

**4** — Module moves and shim management; requires careful migration and testing.

## Maintenance Risk

- Filare-side: Medium during reorg; long-term reduction by clarifying boundaries.
- External: Potential breakage for users importing internal modules; mitigated with shims/deprecation period.
- Ongoing cost: Maintaining shims until downstream consumers migrate.

## Industry / Business Usage

- Libraries often separate CLI from core (e.g., `pytest` core vs. CLI plugin) to keep APIs clean and support embedding.

## Who Uses It & Why It Works for Them

- **Click/Typer-based CLIs**: Thin wrappers over a library core allow reuse without the CLI layer.
- **Data/ETL libraries**: Core pipeline separated from CLI tools to support SDKs and services.

## Feasibility

- Feasible but best aligned with other refactors (pipeline/config) to avoid double migrations; may need staged shims.

## Required Work

- **REWORK tasks**: Define target package layout; move modules (flows/render/models vs. CLI/config/tools) accordingly; add import shims; update entrypoints.
- **FEATURE tasks**: Expose a stable public API surface for embedding; optional SDK doc.
- **DOCUMENTATION tasks**: Migration notes for imports; describe new layout and public modules.
- **TOOLS tasks**: None beyond lint/test fixes; optional script to check for deprecated imports.
- **COVERAGE tasks**: Regression tests for CLI entrypoints and core imports.

## Recommendation

**ADOPT_LATER** — High-value for maintainability/API clarity but should follow pipeline/config groundwork to limit churn.

## References

- Patterns from libraries that separate CLI adapters from core logic to enable embedding and API reuse.
