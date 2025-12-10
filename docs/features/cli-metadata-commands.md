# CLI Commands: metadata domain

uid: FEAT-CLI-0005
status: DONE
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Status
DONE
## Summary

Add `filare metadata <command>` subcommands to inspect, validate, merge, and normalize metadata files. This lets users verify metadata before rendering and reuse merged outputs in pipelines.

## Requirements
- Provide `filare metadata` group with `validate`, `merge`, `describe`, and `edit` subcommands and listed flags/options.
- Support YAML inputs (one or many) and optional schema override for validation; default to built-in schema.
- Emit human-readable output plus optional JSON report where specified; merge can output YAML/JSON, describe supports table/JSON/YAML.
- Honor CLI > ENV > CONFIG > DEFAULT precedence where settings apply; use `pathlib` for paths.
- Keep behavior backward compatible with existing metadata parsing/validation.

## Steps
- [x] Map current metadata parsing/validation flow and available schema helpers to avoid duplication.
- [x] Implement metadata load/merge/validate helpers (with schema override, strict option, source annotations) reusable by CLI.
- [x] Add Typer `metadata` subcommands (`validate`, `merge`, `describe`) with formatting/output flags and exit codes.
- [x] Add Typer `metadata edit` command to launch editor, re-load file, and validate post-edit (with optional skip), respecting schema override.
- [x] Add tests for validation errors/warnings, merge precedence, describe summaries, JSON outputs, and edit flow (editor invocation stub + validation results).
- [x] Update docs/help/examples as needed.

## Progress Log
2025-12-10: Added feature template and implementation plan; status set to IN_PROGRESS pending operator review.
2025-12-10: Implemented metadata CLI (validate/merge/describe/edit), reusable helpers, and tests; marked feature DONE.

## Sub-Features
- None

## Related Issues
- None

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
- `filare metadata edit <file>` — open metadata in user’s editor, then validate after save.
  - Input: single metadata file.
  - Flags: `--schema <path>` (optional schema override), `--strict` (fail on warnings), `--editor <cmd>` (override $EDITOR/$VISUAL), `--no-validate` (skip post-edit validation).
  - Output: exit code based on validation; reprint validation summary after edit.

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

## Implementation
- [x] Audit existing metadata parsing/validation utilities and schema definitions to decide reuse points and default schema resolution.
- [x] Design merge behavior (ordering, override reporting, optional source annotations) and outputs (YAML/JSON) using pathlib paths.
- [x] Implement reusable helpers for validate/merge/describe, then wire Typer subcommands with flags, exit codes, and formatting.
- [x] Add Typer `metadata edit` command to launch editor, re-load file, and validate post-edit (with optional skip), respecting schema override.
- [x] Add focused tests for validation errors/warnings, merge precedence, describe summaries, JSON outputs, and edit flow (editor invocation stub + validation results).
- [x] Update docs/help/examples to reflect new metadata commands and flags.
