from: docs/research/mechanical-diagram-elements.md
uid: FEAT-MECH-0005
status: PROPOSED
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Mechanical Labels and Dimensions

## Status

PROPOSED

## Priority

Medium

## Summary

Add mechanical annotations: labels/markers tied to path positions or features, and dimensions (chain/leader) for segment lengths, clamp spacing, and breakouts.

## Motivation

Board builds and service need clear physical callouts—labels for identification and dimensions for fabrication/QA checks.

## Affected Users / Fields

- Harness manufacturing/QA
- Service technicians
- Mechanical/electrical integration

## Scope

- Labels with text/ID (optional barcode ref) attached to paths/features.
- Dimensions with measurement text, tolerance, and anchor points along paths/features.
- Optional notes for process/environment.

## Out of Scope

- Rendering glyph choices (renderer feature).
- CAD viewer hooks (separate feature).

## Requirements

- Annotations reference paths/features; optional and ignore-safe.
- Dimension supports chain/leader style with units from mechanical block.

## Steps

- [ ] Extend mechanical schema with `annotations` (labels, dimensions, notes) tied to path positions/features.
- [ ] Define allowed fields (text, id, barcode ref, tolerance, anchors).
- [ ] Update docs/examples; ensure renderer can place text/arrows and HTML legend documents symbols.

## Progress Log

- PROPOSED — annotation model defined.

## Validation

- Regression YAML with labels on breakouts/clamps and chain dimensions along a path; render shows callouts.

## Dependencies / Risks

- Depends on base schema/paths; must stay lightweight to avoid cluttered diagrams.
