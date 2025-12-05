# CLI Commands: harness domain

## Summary
Add `filare harness <command>` to build harness artifacts and shared BOM slices, separate from document bundling. This scopes BOM/multiplier tasks and harness-level outputs.

## Commands
- `filare harness render <files...>` — render harness outputs (SVG/PNG/TSV/GV/CSV) without document/title pages.
  - Input: one or more harness YAML files; optional metadata/components.
  - Flags: `-f, --formats <codes>`, `-c, --components <file...>`, `-d, --metadata <file...>`, `-o, --output-dir`, `--use-qty-multipliers`, `-m, --multiplier-file-name`.
  - Output: harness artifacts per file; console summary.
- `filare harness bom <files...>` — generate harness-level BOMs (with optional shared BOM scaling).
  - Input: harness YAML files.
  - Flags: `--use-qty-multipliers`, `-m, --multiplier-file-name`, `-o, --output-dir`, `--format {tsv,csv,json}`.
  - Output: BOM files per harness; optional JSON summary for automation.
- `filare harness stats <files...>` — compute counts/lengths per harness.
  - Input: harness YAML files.
  - Flags: `--format {table,json}`, `--totals` (aggregate across files).
  - Output: stats to stdout/JSON.

## Inputs & Formats
- Harness YAML files plus optional metadata/component overlays.
- Format codes consistent with other domains.

## Outputs
- Harness renders, BOM files, stats summaries; machine-readable options for CI.

## Rationale
- Persona A/D: clearer harness-only tasks without document noise.
- Persona B: explicit BOM generation with multipliers; deterministic outputs.
- Persona C: JSON stats/BOM for pipeline checks.

## Dependencies / Notes
- Integrates with shared BOM logic; reuses multiplier handling.
- Built on Typer hierarchical CLI.

## UI Notes
- Document default multiplier filename/path and provide examples for harness-only vs BOM-only runs.
- Offer JSON outputs for stats/BOM alongside technician-friendly tables.
- Keep format letters aligned with document/page commands to avoid confusion.
