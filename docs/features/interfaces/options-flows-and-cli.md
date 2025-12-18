uid: FEAT-CLI-0018
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: [FEAT-CLI-0016, FEAT-DOCS-0004]
risk: medium
milestone: backlog

# Options Interface Flow and CLI

## Summary

Implement an options interface flow to pull a single options block from a mapping, validate it as `OptionsInterfaceModel`, and expose CLI actions to load/edit/save/check/generate options YAML. Define a sibling `OptionsConfigurationInterfaceModel` (initially empty) for parsing modifiers, and ensure a `FakeOptionsInterfaceFactory` is available for sample generation and tests.

## Usage Targets

- Controls rendering toggles (BOM, cut/termination diagrams, split pages) for HTML/Graphviz outputs.
- Supplies options to downstream export pipelines without touching raw YAML flags.

## Flow Requirements

- Accept `options_map: dict[str, Any]` and `key: str`; raise a keyed error when the selection is absent.
- Apply defaults for all boolean flags when missing; reject non-boolean inputs and unexpected keys before validation.
- Preserve `schema_version` and honor explicit overrides only when provided; emit normalized, lower-case boolean values in YAML.
- Return the validated model and `to_yaml()` output; structure errors with interface type and key for CLI consumption.
- Accept an optional configuration object (`OptionsConfigurationInterfaceModel`) to gate future parsing behavior changes; support `--config <path>` and optional `--config-key` selection (use entire config when omitted).

## CLI Hooks

- `load|check`: read YAML map, pick `--key`, optional `--config/--config-key`, validate, and echo normalized YAML or structured errors.
- `edit`: support flag toggles (`--set include_bom=false`) or open `$EDITOR`/`$VISUAL` via `--editor`, accept `--config/--config-key`, revalidate, and show the resulting state before save.
- `save`: write output YAML/JSON respecting `--output` and `--force`.
- `generate`: rely on `FakeOptionsInterfaceFactory` to emit sample options entries with stable defaults.

## Completion Criteria

- Flow enforces defaulted booleans and forbids extras, matching `OptionsInterfaceModel`.
- CLI supports load/edit/save/check/generate paths for options with consistent UX and exit codes.
