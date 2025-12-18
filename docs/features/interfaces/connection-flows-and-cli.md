uid: FEAT-CLI-0021
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: [FEAT-CLI-0016, FEAT-DOCS-0004]
risk: medium
milestone: backlog

# Connection Interface Flow and CLI

## Summary

Implement a connection interface flow that extracts one connection from a list/map, normalizes aliasing (`from` → `from_`), validates as `ConnectionInterfaceModel`, and exposes CLI actions to manage connection YAML. Define a sibling `ConnectionConfigurationInterfaceModel` (initially empty) for parsing modifiers, and ensure a `FakeConnectionInterfaceFactory` is available for sample generation and tests. Add a dedicated validator in `src/filare/flows/interface/validate_connection.py` to check endpoints against available connectors/cables.

## Usage Targets

- Defines wiring relationships between connectors and cables for internal harness graph construction.
- Supports rendering linkages and driving continuity/validation logic downstream.

## Flow Requirements

- Accept `connections: dict[str, Any] | list[dict[str, Any]]` plus `key: str` (numeric index or explicit id); error if the entry is missing.
- Normalize endpoint keys (`from` alias), enforce that at least one of `from`/`to` is present, and that `via` is always populated.
- Validate endpoints against available connectors/cables when provided as context via a shared validator (`flows/interface/validate_connection.py`); surface errors that include missing designators/pins/wires.
- Preserve `schema_version`; reject extra fields; keep None endpoints when allowed by the model.
- Return the validated model with `to_yaml()`; structure errors to identify which leg (`from`/`via`/`to`) failed.
- Accept an optional configuration object (`ConnectionConfigurationInterfaceModel`) to guide parsing decisions (e.g., endpoint requirements or alias handling); support `--config <path>` and optional `--config-key` (whole config when omitted).

## CLI Hooks

- `load|check`: read connections YAML, select by `--key` (or `--index`), optional `--config/--config-key`, validate with optional `--connectors-file`/`--cables-file` context (allow multiple files per flag), and print normalized YAML or errors.
- `edit`: permit patching endpoints (`--set from.parent=J1 --set via.wire=2`) or open `$EDITOR`/`$VISUAL` via `--editor`, accept `--config/--config-key`, revalidate, and preview the updated triple.
- `save`: write validated YAML/JSON to `--output`, respecting `--force`.
- `generate`: use `FakeConnectionInterfaceFactory` to emit sample connections, with options to force `from`/`to` presence or randomize endpoints.

## Completion Criteria

- Flow enforces alias normalization, endpoint presence rules, and cross-reference checks when context is supplied.
- CLI exposes load/edit/save/check/generate for connections with consistent flags and exit codes.
