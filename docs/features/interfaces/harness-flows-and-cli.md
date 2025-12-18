uid: FEAT-CLI-0022
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: [FEAT-CLI-0016, FEAT-DOCS-0004]
risk: medium
milestone: backlog

# Harness Interface Flow and CLI

## Summary

Implement a harness interface flow that selects one harness definition from a mapping, validates nested metadata/options/connectors/cables/connections via their flows, and exposes CLI actions to manage full-harness YAML. Define a sibling `HarnessConfigurationInterfaceModel` (initially empty) for parsing modifiers, and ensure a `FakeHarnessInterfaceFactory` is available for sample generation and tests.

## Usage Targets

- Serves as the top-level user input feeding internal harness/domain models for rendering and BOM.
- Aggregates nested interface models to drive graph building, document generation, and validation flows.

## Flow Requirements

- Accept `harnesses: dict[str, Any]` and `key: str`; fail clearly if the key is missing or the payload is empty.
- For nested sections, delegate to the respective flows to populate defaults and propagate designators before calling `HarnessInterfaceModel.model_validate`.
- Ensure connectors/cables designators match their mapping keys; propagate to connections so endpoints always reference existing items.
- Keep `schema_version` consistent across nested models; forbid extras at every level and bubble structured validation errors with the failing sub-section noted.
- Return a validated `HarnessInterfaceModel` and `to_yaml()` output; allow `--resolve` flag to inline derived designators in the emitted YAML.
- Accept an optional configuration object (`HarnessConfigurationInterfaceModel`) to steer parsing/normalization policies and pass through to nested flows; support `--config <path>` and optional `--config-key` (whole config when omitted).

## CLI Hooks

- `load|check`: read harness YAML map, select `--key`, optional `--config/--config-key`, run nested validations, and print normalized YAML or structured errors.
- `edit`: accept patches for any nested path (`--set connectors.J1.type=D-Sub`) or open `$EDITOR`/`$VISUAL` via `--editor`, accept `--config/--config-key`, revalidate with nested flows, and show a diff before saving.
- `save`: write validated harness YAML/JSON to `--output`, honoring `--force` for overwrites.
- `generate`: compose `FakeHarnessInterfaceFactory` output, optionally merging user overrides for metadata/options/connectors/cables/connections.

## Completion Criteria

- Flow integrates all interface flows, enforces cross-references, and rejects extra/unmapped connectors or cables.
- CLI supports harness load/edit/save/check/generate with consistent UX, exit codes, and YAML output.
