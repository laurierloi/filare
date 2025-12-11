uid: FEAT-CLI-0010
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# CLI: Interface Commands

## Summary

Add a `filare interface` command set to work directly with interface models: parse YAML into interfaces, generate sample interface YAML, and offer an edit/save workflow.

## Goals

- `filare interface parse <file>`: load user YAML into interface models and report validation details.
- `filare interface example`: emit sample YAML snippets for supported interface models (based on factories).
- `filare interface edit <file>`: open an interface model for interactive editing (non-interactive flags for scripted updates) and save back.
- Reuse `FakeInterfaceFactory`/`Fake<ModelName>Factory` to produce examples and default values.

## Non-Goals

- No schema generation/validation (covered by `filare schema` commands).
- No rendering or BOM operations; this is interface-centric tooling.

## Open Questions

- UX for edit mode (editor launch vs. flags/overrides).
- Where to store/generated sample files (stdout vs. path).
- How to surface adapter info (e.g., mapping to internal models) in command outputs.
