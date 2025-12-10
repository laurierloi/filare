from: docs/research/mechanical-diagram-elements.md

uid: FEAT-MECH-0004
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# Mechanical Features and Coverings

## Status

PROPOSED

## Priority

Medium

## Summary

Add mechanical feature placement (clamps/ties/edge clips, grommets/bulkheads, strain relief/boots/backshells) and protective coverings (conduit/braid/tape/heat-shrink segments) along paths, with part references and placement coordinates/intervals.

## Motivation

Board builds need exact clamp/grommet positions and covering intervals; BOM should reflect these parts with correct quantities.

## Affected Users / Fields

- Harness manufacturing/QA
- Mechanical/electrical integration
- Service (for locating clamps/coverings)

## Scope

- Feature entities with type, position, orientation (optional), part refs, spacing rules.
- Covering entities defined by path intervals (start/end distance) with material/part refs and optional overlap %.

## Out of Scope

- Renderer glyphs (handled by renderer feature).
- Shield/splice/labels (separate features).

## Requirements

- Features and coverings reference paths; support BOM qty multipliers (count or length-based).
- Optional and ignore-safe.
- Allow simple fallback rendering if detailed glyphs are unavailable.

## Steps

- [ ] Extend mechanical schema with `features` (clamp, tie, edge clip, grommet, bulkhead, strain relief/boot/backshell) and placement.
- [ ] Add `coverings` with path ref, start/end distances, material/part refs, overlap %.
- [ ] Update docs/examples; ensure BOM generation can consume part refs/multipliers.

## Progress Log

- PROPOSED — feature/covering placement defined as mechanical elements.

## Validation

- Regression YAML with clamps/grommets and a tape/heat-shrink segment; BOM shows parts; render verifies placement markers.

## Dependencies / Risks

- Needs base schema/paths feature; BOM integration must handle length multipliers for coverings.
