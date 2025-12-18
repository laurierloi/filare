uid: FEAT-CLI-0020
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: [FEAT-CLI-0016, FEAT-DOCS-0004]
risk: medium
milestone: backlog

# Cable Interface Flow and CLI

## Summary

Implement a cable interface flow that extracts a single cable entry from a mapping, backfills the `designator` from the key when missing, validates it as `CableInterfaceModel`, and exposes CLI actions to manage cable YAML. Define a sibling `CableConfigurationInterfaceModel` (initially empty) for parsing modifiers, and ensure a `FakeCableInterfaceFactory` is available for sample generation and tests.

## Usage Targets

- Feeds cable definitions (wirecount, colors, length, shield/type) into internal harness models for rendering and BOM.
- Supplies cable characteristics to connection mapping and downstream validation.

## Flow Requirements

- Accept `cables: dict[str, Any]` and `key: str`; fail clearly when the selection is absent.
- If `designator` is blank, set it from the mapping key; when provided, ensure it matches the key.
- Enforce `wirecount` > 0; if `colors` are provided, require the list length to match `wirecount` or allow empty to defer coloring.
- Normalize optional fields (`length`, `gauge`, `type`, `shield`) and strip whitespace; maintain `schema_version`.
- Return the validated model with `to_yaml()`; include errors that flag wirecount/color mismatches or invalid fields.
- Accept an optional configuration object (`CableConfigurationInterfaceModel`) to steer parsing/normalization changes; support `--config <path>` and optional `--config-key` (use whole config when omitted).

## CLI Hooks

- `load|check`: read cables YAML map, select `--key`, optional `--config/--config-key`, validate, and print normalized YAML or structured errors.
- `edit`: allow updates such as `--set length=\"1 m\"` or color list replacements, or open `$EDITOR`/`$VISUAL` via `--editor`; accept `--config/--config-key`, show a preview diff before saving.
- `save`: write validated cable YAML/JSON honoring `--output` and `--force`.
- `generate`: leverage `FakeCableInterfaceFactory` to emit sample cable entries; support `--count` and `--seed` for reproducibility.

## Completion Criteria

- Flow applies designator propagation, wirecount/color guards, and extra-key forbiddance.
- CLI supports load/edit/save/check/generate for cables with consistent UX and exit codes.
