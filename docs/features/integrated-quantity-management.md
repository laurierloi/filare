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
1) `filare harness qty init examples/demo01.yml -o quantity_multipliers.txt`
2) `filare harness qty edit --set cable1=5`
3) `filare harness qty validate quantity_multipliers.txt --format table`
4) `filare harness qty apply examples/demo01.yml -o outputs/ --format tsv`
5) `filare harness qty report examples/demo01.yml --missing-only`

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
