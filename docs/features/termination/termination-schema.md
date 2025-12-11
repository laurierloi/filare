from: docs/research/termination-diagram-requirements.md

uid: FEAT-TERM-0002
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Termination Schema

## Status

PROPOSED

## Priority

Medium

## Summary

Define an optional termination schema describing how wires/cables terminate into connectors/splices: pin/cavity assignments, terminals/seals, strip lengths, tooling, shield/backshell details, and labels/notes.

## Motivation

Manufacturing and service need explicit pin tables with prep/tooling to assemble or repair connectors correctly.

## Affected Users / Fields

- Harness manufacturing/QA
- Service/diagnostics

## Scope

- Termination entries tied to existing connectors/splices and wires/cables.
- Per-pin/cavity data: assigned wire/conductor, terminal/seal/plug parts, strip length, tooling, shield prep, notes.
- Optional backshell/boot info and labels near connector.

## Out of Scope

- Cut lengths (handled by cut list).
- Detailed 3D models; heavy face diagrams (separate feature if needed).

## Requirements

- Optional top-level `terminations` block; ignore-safe when absent.
- References to connector/splice IDs and wire/cable/wire IDs.
- Fields per pin/cavity: `pin_id/label`, `wire_ref`, `wire_gauge/color`, `terminal_pn`, `seal_pn`, `strip_length`, `tool_crimp`, `tool_extract`, `shield_prep`, `note`.
- Connector-level: `family/type`, `backshell/boot_pn`, `shield_style`, `labels`, `process_ref`.

## Steps

- [ ] Define YAML schema for `terminations` with per-connector/splice entries and per-pin rows.
- [ ] Document schema with examples (sealed connector, shielded cable to backshell, splice).
- [ ] Ensure parser ignores when absent; validate references when present.

## Progress Log

- PROPOSED — termination schema definition.

## Validation

- Regression YAML with terminations for connectors (terminals/seals/tooling) and a shield style; confirm parsing.

## Dependencies / Risks

- Must align with existing connector/cable identifiers; keep optional fields to avoid burdening simple designs.
