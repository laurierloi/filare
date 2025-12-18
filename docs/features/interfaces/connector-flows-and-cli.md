uid: FEAT-CLI-0019
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: [FEAT-CLI-0016, FEAT-DOCS-0004]
risk: medium
milestone: backlog

# Connector Interface Flow and CLI

## Summary

Implement a connector interface flow to extract one connector entry from a mapping, coerce the `designator` from the mapping key when absent, validate as `ConnectorInterfaceModel`, and expose CLI actions to manage connector YAML. Define a sibling `ConnectorConfigurationInterfaceModel` (initially empty) for parsing modifiers, and ensure a `FakeConnectorInterfaceFactory` is available for sample generation and tests.

## Usage Targets

- Drives connector nodes in internal harness models for rendering (pins, loops, styles) and BOM component references.
- Provides connector metadata to graph construction and validation (pin labels/colors, loop visuals).

## Flow Requirements

- Accept `connectors: dict[str, Any]` and `key: str`; error if the key is missing or payload is empty.
- If `designator` is blank, set it to the mapping key before validation; reject mismatches when provided but different.
- Validate pin structures: enforce `pins`, `pinlabels`, and `pincolors` list lengths consistency when more than zero are supplied; ensure loop endpoints reference known pins/pinlabels.
- Normalize optional fields (`type`, `subtype`, `style`) and strip whitespace; keep ordering stable for YAML output.
- Return the validated model with `to_yaml()`; include structured validation errors naming the offending pin/loop when failures occur.
- Accept an optional configuration object (`ConnectorConfigurationInterfaceModel`) to influence parsing/normalization rules as they emerge; support `--config <path>` and optional `--config-key` (use the whole config when omitted).

## CLI Hooks

- `load|check`: read connectors YAML map, select `--key`, optional `--config/--config-key`, populate designator, validate, and print normalized YAML or errors.
- `edit`: allow pin/loop updates via `--set pinlabels[0]=...`, patch files, or open `$EDITOR`/`$VISUAL` via `--editor`; accept `--config/--config-key`, revalidate, and preview the diff.
- `save`: write validated YAML/JSON to `--output`, gated by `--force` for overwrites.
- `generate`: use `FakeConnectorInterfaceFactory` to emit sample connectors keyed by provided IDs; allow `--count` and `--style simple` overrides.

## Completion Criteria

- Flow enforces designator propagation, pin/loop sanity, and forbids extras.
- CLI exposes connector load/edit/save/check/generate paths with consistent options and exit codes.
