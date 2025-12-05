# CLI Commands: metadata domain

## Summary
Add `filare metadata <command>` subcommands to inspect, validate, merge, and normalize metadata files. This lets users verify metadata before rendering and reuse merged outputs in pipelines.

## Commands
- `filare metadata validate <files...>` — validates metadata YAML files against schema.
  - Input: one or more YAML metadata files.
  - Flags: `--schema <path>` (optional schema override), `--strict` (fail on warnings).
  - Output: exit code, validation report to stdout; optional JSON report with `--json`.
- `filare metadata merge <files...>` — merges multiple metadata files in order.
  - Input: ordered YAML metadata files.
  - Flags: `-o, --output <path>` (write merged YAML), `--format {yaml,json}` (output format), `--show-source` (annotate keys with source file).
  - Output: merged metadata written to file/stdout; summary of overrides.
- `filare metadata describe <file>` — prints key fields and defaults for quick inspection.
  - Input: single metadata file.
  - Flags: `--format {table,json,yaml}`.
  - Output: human-readable summary to stdout.

## Inputs & Formats
- YAML files following Filare metadata schema; allow multiple files for merge/validate.
- Optional schema path for validation; defaults to built-in schema.

## Outputs
- Validation: success/failure exit code; human summary; optional machine-readable JSON report.
- Merge: merged metadata file (YAML/JSON) and override summary.
- Describe: tabular or JSON summary to stdout.

## Rationale
- Persona A/D: quick feedback on metadata correctness without rendering.
- Persona B: deterministic merging order and override visibility.
- Persona C: machine-readable reports for CI gating.

## Dependencies / Notes
- Build on Typer hierarchical CLI (docs/features/cli-typer-migration.md).
- Align defaults and schema references with existing docs/tutorials.

## UI Notes
- Provide examples for validate/merge/describe with multiple files and ordering.
- Surface default schema path and show how to emit JSON reports for CI alongside table output.
- Clarify how conflicts are reported (source file/line when available).
