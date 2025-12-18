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

## Implementation Assessment (2025-02-04)

- Current support: No `interface` CLI group; interface models exist under `filare.models.interface` but unused in CLI.
- Clarity: Goals clear; need UX decisions for edit flow (non-interactive vs editor) and output locations.
- Difficulty: Medium — requires building parsers around existing models and adding Typer commands plus tests.
- Reuse `FakeInterfaceFactory`/`Fake<ModelName>Factory` to produce examples and default values.

## Non-Goals

- No schema generation/validation (covered by `filare schema` commands).
- No rendering or BOM operations; this is interface-centric tooling.

## Open Questions

- UX for edit mode (editor launch vs. flags/overrides).
- Where to store/generated sample files (stdout vs. path).
- How to surface adapter info (e.g., mapping to internal models) in command outputs.
