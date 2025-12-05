# CLI Commands: settings domain

## Summary

Add `filare settings <command>` to read, update, and persist Filare settings (paths, defaults, format preferences), improving transparency and reproducibility.

## Commands

- `filare settings show` — display current settings and defaults.
  - Input: none (reads from config file/environment).
  - Flags: `--format {table,json,yaml}`, `--include-defaults`.
  - Output: settings to stdout.
- `filare settings set <key> <value>` — update a setting (e.g., default formats, output dir).
  - Input: key/value.
  - Flags: `--scope {user,project}`, `--type {string,bool,int,list}` (optional for parsing), `--append` (for list types).
  - Output: confirmation and new value.
- `filare settings reset [<key>]` — reset one or all settings to defaults.
  - Input: optional key.
  - Flags: `--scope {user,project}`, `--yes` (non-interactive).
  - Output: confirmation summary.
- `filare settings path` — print config file path(s).
  - Input: none.
  - Flags: `--create` (create if missing).
  - Output: path to stdout.

## Inputs & Formats

- No YAML inputs; operates on config files/env.
- Supports JSON/YAML output for automation.

## Outputs

- Human-readable or machine-readable settings summaries; confirmation messages; exit codes for CI.

## Rationale

- Persona A/D: clear defaults and easy tweaks without editing files manually.
- Persona B/C: reproducible, scoped settings with machine-readable output for pipelines.

## Dependencies / Notes

- Requires defined settings storage format (per-user/project) and schema.
- Built on Typer hierarchical CLI; ensure backward compatibility for existing defaults.

## UI Notes

- Show config file locations and scopes in help (`user` vs `project`) with examples.
- Ensure outputs support both table and JSON for automation.
- Provide non-interactive flags (`--yes`) and clear error messages when scope/key is invalid.
