from: docs/features/standard-harness-component-support.md

# Shield Termination Metadata

## Status

PROPOSED

## Priority

High

## Summary

Capture how shielded cables terminate (drain target, backshell/pigtail, isolation/continuity) so diagrams and BOM reflect EMI/grounding intent, not just the presence of a shield.

## Motivation

- Aero/defense and automotive EMI compliance depends on explicit shield termination style and location.
- Service and manufacturing need to know whether to tie shield to backshell, pigtail to ground, or leave isolated.

## Affected Users / Fields

- Aerospace/defense wiring teams
- Automotive harness engineers (shielded sensor/data lines)
- Harness manufacturing and service technicians

## Scope

- New metadata on cables/connectors to describe shield termination target and style.
- Diagram symbols for shield drain to ground/backshell/pigtail; BOM entries for backshell/ground hardware when specified.
- Backward compatible defaults (no change when unspecified).

## Out of Scope

- Detailed EMI simulation or impedance modeling.

## Requirements

- Optional shield termination block (e.g., style: backshell/pigtail/isolated; target connector/pin or stud; note).
- Ability to associate backshell/ground hardware as BOM items when specified.
- Diagram rendering that shows termination glyph (drain to ground lug, backshell symbol, or isolated).
- Should not alter behavior for existing shielded cables lacking the new block.

## Steps

- [ ] Define schema additions for shield termination metadata on cables (and optional connector-side reference).
- [ ] Update rendering to show shield termination glyphs and target labels.
- [ ] Extend BOM handling to include backshell/ground hardware when present.
- [ ] Document syntax and add regression YAML covering different termination styles.
- [ ] Validate HTML/Graphviz outputs and BOM.

## Progress Log

- PROPOSED — sub-feature extracted from standard harness component support.

## Validation

- Regression YAML with shielded cable showing: (1) backshell termination, (2) pigtail-to-ground, (3) isolated shield; BOM includes backshell/ground hardware when specified.

## Dependencies / Risks

- Symbol choices must align with existing visual style.
- Need clear default when style not specified (assume current behavior: simple shield line).
