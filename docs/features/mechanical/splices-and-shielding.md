from: docs/research/mechanical-diagram-elements.md
uid: FEAT-MECH-0006
status: PROPOSED
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Mechanical Splices and Shield Terminations

## Status

PROPOSED

## Priority

Medium

## Summary

Represent mechanical placement of splices/junctions and shield terminations along paths, with symbols, part references, and linkage to electrical wires/connectors.

## Motivation

Manufacturing and service need to locate splices and understand shield termination style (backshell, pigtail, isolated) on the physical layout.

## Affected Users / Fields

- Harness manufacturing/QA
- Service/diagnostics
- EMI/packaging reviewers

## Scope

- Splice/junction entities: position, type (inline barrel, junction block), part ref, involved wires/nets.
- Shield termination entities: path endpoint or connector association, style (backshell/pigtail/isolated), target (ground stud/backshell), hardware refs.

## Out of Scope

- Electrical rules beyond presence/location.
- Renderer glyphs (handled by renderer feature).

## Requirements

- Link splices to wires/cables/connectors for traceability.
- Shield terminations tie to connector/path end; optional hardware for BOM.
- Optional and ignore-safe in YAML.

## Steps

- [ ] Add `splices` to mechanical schema with position, type, part ref, wire/net refs.
- [ ] Add `shield_terminations` with style/target/hardware refs tied to path ends/connectors.
- [ ] Update docs/examples; ensure BOM picks up part refs and hardware.

## Progress Log

- PROPOSED — mechanical splice and shield placement defined.

## Validation

- Regression YAML with an inline splice and a shield termination to backshell/ground; render shows markers and BOM lists parts.

## Dependencies / Risks

- Needs base schema/paths; relies on consistent wire identifiers to link mechanical and electrical views.
