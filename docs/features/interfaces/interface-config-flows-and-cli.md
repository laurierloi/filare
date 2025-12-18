uid: FEAT-CLI-0023
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: [FEAT-CLI-0016]
risk: medium
milestone: backlog

# Interface Configuration Flows and CLI

## Summary

Provide a unified configuration model and CLI for interface parsing behavior. Configs have four levels: global (applies to all interfaces), default (per-interface-type defaults), type (named config per interface type), and item (per interface key). A Typer-based `filare interface-config` CLI must edit/update/check/generate configs and feed `--config`/`--config-key` into interface flows.

## Config Model Requirements

- Define configuration models per interface type under `src/filare/models/interface/`, plus a top-level config schema capturing the four levels.
- Levels:
  - Global: baseline applied to every interface.
  - Default: per interface type defaults when no type-specific config is given.
  - Type: explicit config chosen for a given interface type via `--config-key`.
  - Item: config keyed by interface ID that overrides higher levels for that specific item.
- Support YAML/JSON round-trip and forbid extras; preserve `schema_version`.

## CLI Behavior

- Command shape: `filare interface-config <action> [OPTIONS]` with actions `load|edit|save|check|generate`.
- Accept `--config <path>` and optional `--config-key` to target a type or item config; fall back to whole config when no key is provided.
- `load|check`: read config, validate across all levels, and report structured errors.
- `edit`: allow `--set`/`--patch` or open `$EDITOR`/`$VISUAL` via `--editor`, revalidate, and preview diff.
- `save`: write validated config to `--output`, guarded by `--force`.
- `generate`: emit sample configs for all interface types leveraging fake factories where helpful.

## Integration with Interface Flows

- All interface flows must accept an optional config object and optional `config_key`; when absent, apply the merged effective config (global → default → type → item).
- Ensure CLI commands for interfaces forward `--config`/`--config-key` to flows and use the resolved effective config during validation/normalization.
