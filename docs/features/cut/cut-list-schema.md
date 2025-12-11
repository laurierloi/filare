from: docs/research/cut-diagram-requirements.md

uid: FEAT-BOM-0003
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Cut List Schema

## Status

PROPOSED

## Priority

Medium

## Summary

Define an optional cut-list schema to describe wire/cable cutting instructions: length, part references, end prep per side, labels, and breakouts for cables. This enables Filare to generate cut sheets for shop-floor use.

## Motivation

Manufacturing needs precise lengths, strip/crimp prep, labels, and breakout instructions to program cutting/strip/tin equipment and prepare terminations.

## Affected Users / Fields

- Harness manufacturing/QA
- Service (for replacement reference)

## Scope

- Cut-list entries tied to existing wires/cables/connectors.
- Fields for length/tolerance, material reference (MPN, gauge, color), end prep per side, labels, shield prep, breakouts.
- Optional fields to keep simple cases lightweight.

## Out of Scope

- Graphical line sketches (separate feature if needed).
- Machine-specific formats (beyond CSV/TSV export).

## Requirements

- Optional top-level `cut_list` block; ignore-safe when absent.
- Link entries to `cables`/`wires` and connector ends.
- Per-side prep: strip length, terminal/seal/plug part, tool ref, shield prep note, boot/heat-shrink/tape note.
- Labels with text/position/part/template.
- Breakouts for cables with positions and conductor assignment.
- Notes/tolerance and process references (IPC/WHMA).

## Steps

- [ ] Define YAML schema for `cut_list` entries with required/optional fields and references to existing design objects.
- [ ] Document schema and provide examples (wire, shielded cable with breakouts).
- [ ] Ensure parser ignores block when absent; validate links when present.

## Progress Log

- PROPOSED — cut-list schema definition.

## Validation

- Regression YAML containing cut_list entries for wires and multi-conductor cables; confirm parsing and field presence.

## Dependencies / Risks

- Must align identifiers with existing cables/wires/connectors; avoid breaking existing files.
