# CLI Commands: settings domain

## Status

DONE

## Summary

Add `filare settings <command>` to read, update, and persist Filare settings (paths, defaults, format preferences), improving transparency and reproducibility.

## Requirements

- Provide a `filare settings` command group with `show`, `set`, `reset`, and `path` subcommands plus listed flags.
- Support per-user and per-project scopes with clear precedence and explicit config file locations.
- Default config directory is `$XDG_CONFIG_HOME/filare`, overridable via `FIL_CONFIG_PATH`; settings stored as YAML files named per scope (e.g., `<name_of_settings>.yaml`).
- Offer YAML output and human-readable table formatting (no JSON option for now).
- Settings resolution priority: CLI args override env vars, which override config file values, which override defaults.
- Maintain backward compatibility with existing defaults and environment-variable overrides; use `pathlib` for all path handling.

## Steps

- [x] Map current settings loading (env + defaults) and decide config storage locations/schema for user/project scopes.
- [x] Implement settings persistence and resolution (defaults, env, user, project) plus helpers to read/write and validate values.
- [x] Add Typer `settings` command group with `show`, `set`, `reset`, and `path` behaviors and formatting flags.
- [x] Add tests covering settings loading, precedence, mutations, and CLI outputs.
- [x] Update docs/help text and examples as needed.

## Progress Log

2025-12-10: Created feature plan and initial status.
2025-12-10: Implemented YAML-backed settings store (FIL_CONFIG_PATH/XDG paths), Typer commands, and tests for precedence and mutations.
2025-12-10: Updated feature doc; marked feature DONE pending operator review.
2025-12-10: Added `just filare-settings-get` helper to show resolved settings.
2025-12-10: Added `config_dir` read-only setting surfaced in `settings show`.

## Sub-Features

- None

## Related Issues

- None

## Commands

- `filare settings show` — display current settings and defaults.
  - Input: none (reads from config file/environment).
  - Flags: `--format {table,yaml}`, `--include-defaults`.
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

- operates on config files/env/yaml.
- Supports YAML output for automation.

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
- Ensure outputs support both table and YAML for automation.
- Provide non-interactive flags (`--yes`) and clear error messages when scope/key is invalid.

## Implementation

- [x] Analyze existing `filare.settings` usage to decide new storage schema (keys, types, defaults) and confirm env override strategy (`FIL_CONFIG_PATH` vs `$XDG_CONFIG_HOME/filare`).
- [x] Define config path resolution for `user` vs `project` scopes using `pathlib`, including creation behavior for `settings path --create` and file naming (`<name_of_settings>.yaml`).
- [x] Implement YAML-only settings persistence/merging helpers (load/write, type parsing, append semantics) to back the CLI.
- [x] Wire Typer `settings` subcommands (`show`, `set`, `reset`, `path`) to the persistence layer with format/scoping flags (table/YAML) and exit codes.
- [x] Add tests for settings resolution and CLI commands; refresh docs/help to reflect new behaviors.
