# Metadata Configuration Harmonization

## Summary

Proposes harmonizing metadata ingestion (YAML metadata files, CLI overrides, env-driven defaults) into a unified, typed metadata configuration loaded via the same `src/filare/config/` layer. Today, metadata is parsed separately and mixed with ad-hoc dicts (`extra_metadata`) in the pipeline; unifying it would give a single source of truth for document/harness metadata and simplify downstream rendering logic.

## Use Cases for Filare

- Consistent metadata across title pages, harness pages, BOM, and PDF bundling without re-parsing or manual merging.
- Easier CI/local overrides of metadata fields (e.g., project name, revision, approvers) via env/flags.
- Predictable metadata structure for downstream consumers (APIs, validators, docs tooling).

## Technical Evaluation

- Features: Typed metadata config model (project info, revision, sheet counters, author/approver fields, custom fields) resolved from env/CLI/metadata files. Single merge step producing a resolved metadata object consumed by rendering flows.
- Strengths: Eliminates duplicated parsing/merging; improves validation; simplifies titlepage/index generation; prepares for future API exposure.
- Weaknesses: Migration effort to replace current `parse_metadata_files` + `extra_metadata` merging; must keep YAML schema backward compatible.
- Limitations: Needs careful field mapping to avoid breaking existing metadata YAML files; may need deprecation shims.
- Compatibility with Filare: Fits with planned config unification; uses Pydantic models for validation.
- Required integrations: Extend config loader to include metadata layer; adjust flows to consume resolved metadata instead of ad-hoc dicts.

## Complexity Score (1–5)

**3** — Moderate: new models and merge logic, plus flow adjustments; limited algorithmic risk.

## Maintenance Risk

- Filare-side: Medium during migration; long-term reduction by centralizing metadata handling.
- External: None; relies on existing YAML inputs; requires clear backward-compat policy.
- Ongoing cost: Low once unified; adding fields becomes a model change with validation.

## Industry / Business Usage

- Documentation/build systems (Sphinx/MkDocs) and EDA tools rely on centralized metadata/config to populate headers/footers and build artifacts consistently.

## Who Uses It & Why It Works for Them

- **Sphinx/MkDocs**: Single config drives metadata across all generated pages.
- **EDA/PLM exports**: Central project metadata cascades into BOMs, drawings, and change requests, reducing drift.

## Feasibility

- Feasible now, especially alongside configuration-layer unification and pipeline/context refactor.

## Required Work

- **REWORK tasks**: Define typed metadata model and merge strategy (file → CLI/env overrides); integrate into `src/filare/config/`; replace `extra_metadata` mutations with the resolved metadata object.
- **FEATURE tasks**: Optional metadata overlay files or profiles (e.g., `metadata.dev.yml`, `metadata.release.yml`) resolved by environment.
- **DOCUMENTATION tasks**: Document metadata precedence, supported fields, and how to override via env/flags; include migration guidance for existing YAML metadata files.
- **TOOLS tasks**: Add a `filare metadata show`/validation command to dump resolved metadata.
- **COVERAGE tasks**: Tests for precedence, backward compatibility, and rendering outputs using the unified metadata.

## Recommendation

**ADOPT_LATER** — Pair with configuration unification/pipeline refactor to minimize churn while keeping backward compatibility with existing metadata files.

## References

- SSG and PLM metadata handling patterns (single config driving multiple generated artifacts).

## Optional Appendix

- Example precedence: `metadata.yml` → env overrides (`FIL_META_*`) → CLI flags (e.g., `--project-name`, `--rev`) → resolved metadata object passed to flows.
