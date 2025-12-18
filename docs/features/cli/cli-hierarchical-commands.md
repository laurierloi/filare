# Hierarchical CLI for Filare (metadata/document/page/harness/settings/drawio)

uid: FEAT-CLI-0004
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Introduce a unified, multi-level CLI (`filare <domain> <command>`) so users can target specific parts of the flow (metadata, documents, pages, harnesses, settings, drawio). This improves discoverability, enables segmented validation, and reduces cognitive load compared to separate executables.

## Motivation (Personas)

- Persona A/D: Need clear, task-focused commands (e.g., “render one page” or “update metadata”) without guessing flags or separate tools.
- Persona B: Wants deterministic, segmented flows to validate each stage (metadata → harness → document → bundle).
- Persona C: Needs stable, scriptable subcommands with predictable names and options for CI.

## Implementation Assessment (2025-02-04)

- Current support: Typer root exists with `run`, `qty`, `settings`, `metadata`, `drawio`; missing `document`, `harness`, `page`, `interface`, `schema`, and code-analysis domains.
- Clarity: Target domains are enumerated; need decisions on nesting order and backward-compatible aliases.
- Difficulty: Medium — requires reorganizing existing Typer apps and adding new stubs while keeping legacy `filare run` path functional.

## Implementation Plan (next steps)

- Introduce new Typer groups incrementally (start with `harness` and `document/page` as they reuse existing flows).
- Keep `filare run` as a backward-compatible alias during transition; document deprecation path.
- Update `cli.main` wiring and CLI help to reflect the hierarchy; add smoke tests for new entrypoints.
- Defer interface/schema/code domains to later phases once scoped.

## Proposal

- Restructure CLI into domains:
  - `filare metadata <cmd>` — inspect/merge/validate metadata files.
  - `filare document <cmd>` — configure or render full document bundles (HTML/PDF, title page).
  - `filare page <cmd>` — operate on a single page/sheet (render, export formats).
  - `filare harness <cmd>` — build harness outputs and shared BOM slices.
  - `filare settings <cmd>` — read/update/write Filare settings (paths, defaults).
  - `filare drawio <cmd>` — manage Draw.io integrations (import/export/sync).
- Provide a top-level `filare help` that lists domains and key commands with one-line descriptions and examples.
- Keep format/output options scoped to relevant domains; avoid cross-domain flag meaning conflicts.
- Support segmented execution for verification (e.g., `metadata validate`, then `harness render`, then `document bundle`), surfacing clear outputs and exit codes per step.
- Maintain backward-compatible aliases (`filare` existing default render, `filare-qty`) for a deprecation window with help text pointing to new subcommands.

## User Impact

- Faster onboarding: users see available domains instead of guessing extra executables.
- Better correctness: each stage can be run and verified separately in pipelines.
- Reduced flag confusion: domain-scoped options and consistent naming.

## Dependencies / Considerations

- Requires CLI restructuring (see related Typer migration feature).
- Documentation updates: help text, examples, workflows, and tutorials must mirror new command tree.
- Backward compatibility strategy for existing scripts (`filare`, `filare-qty`).

## Related

- docs/features/cli-typer-migration.md
- docs/issues/cli-subcommand-discovery.md

## UI Notes

- Add `filare help` command map showing all domains and top tasks, with copy/paste examples.
- Keep short flags consistent across domains; avoid reusing `-f` for different meanings.
- Provide per-domain default paths and outputs inline in help (e.g., output dir, multiplier file).
