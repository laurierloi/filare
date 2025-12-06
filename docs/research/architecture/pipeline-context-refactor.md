# Pipeline Context & Orchestrator Refactor

## Summary

Proposes replacing ad-hoc dictionaries and implicit globals (e.g., `extra_metadata`, `shared_bom` in `cli.py`/`filare.parse`) with an explicit pipeline orchestrator and immutable-ish context objects. The goal is to make parsing/rendering flows composable, testable, and easier to extend (cut/termination diagrams, BOM) without mutating shared state across functions.

## Use Cases for Filare

- Running multiple render passes (HTML/SVG/PNG/PDF) without duplicated preamble logic.
- Enabling alternate entrypoints (CLI, API, harness runners) that share a common pipeline.
- Simplifying integration of future steps (validation, profiling hooks, caching) via pipeline stages.
- Making per-page/page-set metadata deterministic for downstream viewers/validators.

## Technical Evaluation

- Features: Introduce a `PipelineContext` (dataclass/Pydantic) that carries inputs, options, derived metadata, and accumulator fields (shared BOM, notes). Add a small orchestrator that executes registered stages (parse metadata, build harness, render formats, assemble bundles).
- Strengths: Eliminates mutable default args (`extra_metadata={}`, `shared_bom={}`); isolates stage responsibilities; makes it easier to unit-test each stage; provides a single place to plug metrics/profiling.
- Weaknesses: Requires touching many call sites; needs careful migration to avoid regressions.
- Limitations: Short-lived CLI runs might not benefit from heavier orchestration unless kept lightweight.
- Compatibility with Filare: Fits current flow modules (`flows/`, `render/`); can wrap existing functions in staged adapters.
- Required integrations: Define context model(s), stage registry, and adapters around `build_harness_from_files`, `build_shared_bom`, `build_titlepage`, and PDF bundling.

## Complexity Score (1–5)

**3** — Moderate refactor: new context model and orchestrator, plus migration of CLI/flows to use them. Limited algorithm changes but touches multiple modules.

## Maintenance Risk

- Filare-side: Medium risk during migration (state leakage, ordering). Once adopted, reduces risk by clarifying data flow.
- External: None; uses stdlib/dataclasses/Pydantic already in use.
- Ongoing cost: Low; stages are explicit, making future additions predictable.

## Industry / Business Usage

- Data/ETL and rendering tools (e.g., Pandas pipelines, Airflow DAG tasks) use explicit contexts to keep runs reproducible and debuggable.
- CLI tools with multi-output workflows (e.g., Sphinx, MkDocs builds) rely on structured build contexts to avoid duplicated setup/teardown per output format.

## Who Uses It & Why It Works for Them

- **Sphinx/MkDocs**: Build context carries config, source tree, and output targets, enabling concurrent builders and incremental runs.
- **Airflow DAG operators**: Task context provides run metadata and shared variables, reducing implicit global state.
- **Static site generators**: Pipeline stages (parse → transform → render) improve caching and partial rebuilds.

## Feasibility

- Feasible now; requires a focused refactor of CLI/flows. Could be phased by wrapping existing functions in context-aware adapters before removing old signatures.

## Required Work

- **REWORK tasks**: Introduce `PipelineContext` (inputs, output_dir, formats, metadata, shared_bom, sheet counters); replace mutable defaults in `filare.parse`/CLI; wrap existing flow functions as stages; add simple orchestrator to run stages in order.
- **FEATURE tasks**: Optional stage registry for custom render steps (cut/termination, BOM variants) and hooks for metrics/profiling/caching.
- **DOCUMENTATION tasks**: Developer doc explaining pipeline stages, context fields, and how to add/remove stages.
- **TOOLS tasks**: None immediate; optional tracing hooks for debugging.
- **COVERAGE tasks**: Add focused unit tests for stage execution order and context mutation guarantees.

## Recommendation

**ADOPT_LATER** — Plan a staged refactor to introduce a pipeline/context while keeping current behavior stable; schedule alongside other CLI/flow cleanup.

## References

- Patterns from SSG/ETL orchestrators (Sphinx/MkDocs build context, Airflow task context) as analogous structures.

## Optional Appendix

- Example stage chain: `ingest_inputs -> load_components -> parse_harness -> render_formats -> aggregate_shared_bom -> build_titlepage -> bundle_pdf`.
