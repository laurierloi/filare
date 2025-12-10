from: docs/research/mechanical-diagram-elements.md

uid: FEAT-MECH-0003
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# Mechanical Base Schema and Paths

## Status

PROPOSED

## Priority

Medium

## Summary

Define an optional `mechanical` block that captures units/datum, board/fixture outline, reference holes, and harness paths (polylines, breakouts, segment metadata) to anchor all mechanical elements.

## Motivation

Mechanical overlays require structured geometry (outline, paths, points) before clamps, coverings, splices, or dimensions can be placed.

## Affected Users / Fields

- Harness manufacturing/QA (board setups)
- Mechanical/electrical integration teams

## Scope

- New `mechanical` schema: units, datum/grid, outline polygon, reference holes.
- Path definitions with points, segment lengths/bend radii, and breakout markers tied to cables/connectors.

## Out of Scope

- Rendering and symbols (handled by renderer feature).
- Coverings/fixtures/splices (separate features).

## Requirements

- Optional and ignore-safe: existing YAMLs remain valid.
- Paths reference existing cables/connectors/wires for traceability.
- Support per-segment metadata (length, bend radius placeholder).

## Steps

- [ ] Design YAML structure for `mechanical` (units, datum/grid, outline, reference holes).
- [ ] Define `paths` with point lists, breakout markers, and linkage to cables/connectors.
- [ ] Add docs and example YAML; ensure parser ignores block when absent.

## Progress Log

- PROPOSED — initial base schema definition.

## Validation

- Regression YAML with mechanical outline + paths; confirmed parsed without affecting existing renders.

## Dependencies / Risks

- Must not conflict with existing top-level keys; needs clear defaults for units/datum.
