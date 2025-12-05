# Integrated Quantity Management in Filare

## Summary

Fold quantity multiplier management into the main Filare CLI (no separate `filare-qty`), with clear subcommands, defaults, and reports. Users can create, edit, validate, and apply multipliers directly alongside harness rendering.

## Goals

- One unified CLI tree: quantity tasks live under Filare, discoverable via `filare harness qty` (or `filare quantity` alias).
- Clear defaults and file paths (e.g., `quantity_multipliers.txt` in project root unless overridden).
- Machine-readable reports for CI, plus human-friendly prompts for technicians.

## Proposed Commands

- `filare harness qty init <files...>`
  - Purpose: bootstrap multipliers from harness files.
  - Inputs: harness YAML files.
  - Flags: `-o, --output <path>` (default `quantity_multipliers.txt`), `--force` (overwrite), `--format {txt,json,yaml}`.
  - Output: multiplier file; summary of parts needing multipliers.
- `filare harness qty edit [<path>]`
  - Purpose: interactive or inline edits to multiplier file.
  - Inputs: optional multiplier file path (default `quantity_multipliers.txt`).
  - Flags: `--set key=value`, `--remove key`, `--format {txt,json,yaml}`, `--non-interactive` (fail if missing entries).
  - Output: updated file; diff summary to stdout.
- `filare harness qty validate <path>`
  - Purpose: ensure multiplier file is well-formed and matches harness parts.
  - Inputs: multiplier file; optional harness files for cross-check.
  - Flags: `--format {table,json}`, `--strict` (fail on missing entries), `--schema <path>` if YAML/JSON.
  - Output: validation report; exit code for CI.
- `filare harness qty apply <files...>`
  - Purpose: render shared BOM with multipliers applied.
  - Inputs: harness YAML files; multiplier file.
  - Flags: `-m, --multiplier-file <path>` (default `quantity_multipliers.txt`), `-o, --output-dir`, `--format {tsv,csv,json}`, `--dry-run` (report only).
  - Output: scaled shared BOM files; summary report.
- `filare harness qty report <files...>`
  - Purpose: show which multipliers were used/missing after a render.
  - Inputs: harness YAML files; multiplier file.
  - Flags: `--format {table,json}`, `--missing-only`.
  - Output: usage/missing report to stdout; JSON for automation.

## Inputs & Formats

- Harness YAML files (existing schema).
- Multiplier file default: `quantity_multipliers.txt`; support TXT (key=value), JSON, or YAML for structured data.
- Paths relative to project root unless absolute.

## Outputs

- Multiplier files (txt/json/yaml).
- Validation and usage reports (table/json) to stdout or `--output`.
- Shared BOM files (tsv/csv/json) when applying.
- Exit codes suitable for CI gating.

## Workflow (example)

1. `filare harness qty init examples/demo01.yml -o quantity_multipliers.txt`
2. `filare harness qty edit --set cable1=5`
3. `filare harness qty validate quantity_multipliers.txt --format table`
4. `filare harness qty apply examples/demo01.yml -o outputs/ --format tsv`
5. `filare harness qty report examples/demo01.yml --missing-only`

## UX Considerations

- Surface defaults inline in help and in `filare help` command map.
- Keep short flags consistent across domains (avoid `-f` meaning different things).
- Offer `--json` everywhere for Persona C, and concise tables for Personas A/D.
- Provide clear messages when entries are missing, with suggested `edit` commands.

## Compatibility

- Keep `filare-qty` as a shim initially, printing a deprecation notice and redirecting to `filare harness qty`.
- Honor existing default filename (`quantity_multipliers.txt`) to avoid breaking current users.

## Dependencies

- Depends on Typer-based hierarchical CLI (docs/features/cli-typer-migration.md).
- Requires structured multiplier parser (txt/json/yaml) and shared BOM integration points.

## Data & Formats (Implementation Detail)

- Default file name: `quantity_multipliers.txt` in project root unless `-m/--multiplier-file` is provided.
- TXT format: one `key=value` per line, `#` for comments; keys match harness part identifiers; values are numeric (int/float).
- JSON/YAML format: flat map of `{key: number}`; support optional metadata block `{version, generated_at, source_files}` for traceability.
- Order of harness files: maintain sorted order unless `--order` is specified elsewhere; report the order used.

## Validation Rules

- Detect missing multiplier entries for referenced parts (strict mode fails).
- Detect unused entries (warn).
- Reject non-numeric values or duplicate keys with differing values.
- Report source file and line (when available) for TXT/structured formats.

## Reports (Machine-Friendly)

- `--format json` outputs shape:
  ```json
  {
    "status": "ok|error|warning",
    "file": "quantity_multipliers.txt",
    "missing": ["partA", "partB"],
    "unused": ["oldPart"],
    "applied": { "partA": 5, "partC": 2 },
    "errors": [{ "key": "partX", "message": "non-numeric", "line": 12 }]
  }
  ```
- Table output mirrors these fields in human-readable form.

## Non-Interactive & CI Behavior

- All commands must support non-interactive mode (no prompts) with deterministic exit codes:
  - 0: success (and warnings only if `--strict` not set)
  - 1: validation/application errors
  - 2: usage/config errors
- `--dry-run` available on apply/report to avoid writing outputs during CI checks.

## Backward Compatibility / Migration

- Phase 1: `filare-qty` remains; prints deprecation notice and delegates to `filare harness qty ...`.
- Phase 2: Warning escalates; help text points to new commands and examples.
- Phase 3: Remove shim after major release (document timeline in changelog).

## Implementation Notes

- Centralize multiplier parsing/serialization for TXT/JSON/YAML to avoid drift.
- Reuse shared BOM flow; inject multipliers early and emit per-harness + aggregated reports.
- Add examples to `examples/` showing multiplier files in each format.
- Update workflows/tutorials to include the new commands and `--json` reporting for CI.

## UI Notes

- Surface defaults prominently in help (filename/location, strict vs non-strict) and keep examples copy/paste ready.
- Ensure `--json` mirrors human table fields to reduce context switching for technicians vs CI.
- Provide error messages that cite missing/unused keys and suggest next commands (`validate` then `edit`).
