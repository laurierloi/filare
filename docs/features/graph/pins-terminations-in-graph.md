from: docs/features/graph/pins-in-graph.md

uid: FEAT-GRAPH-0014
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# Pins–Terminations in Graph

## Status

PLANNED

## Summary

Model terminations (splice, crimp, solder, etc.) as graph nodes and link pins to terminations via FilareLink-based edges to represent physical/electrical joining without embedding termination data in pins or connectors.

## Requirements

- Define a Termination node type (FilareModel-backed) with UUID4 ID and termination metadata (type/kind, side, tooling notes).
- Link pins to terminations via dedicated links (e.g., PinTerminationLink) carrying role/position metadata if needed.
- Preserve legacy termination representations (if present) by generating nodes/links during parsing; keep outputs backward compatible.
- Keep rendering/BOM behavior stable; termination links augment data without breaking current flows.

## Steps

- [ ] Design Termination node schema and PinTerminationLink payload (roles/position).
- [ ] Implement termination node creation and pin-to-termination link generation during parsing; adapt any legacy fields.
- [ ] Update render/BOM flows to consume termination links where applicable.
- [ ] Add tests/examples and documentation; ensure legacy outputs remain unchanged by default.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec for representing terminations as graph nodes linked from pins.

## Sub-Features

- None

## Related Issues

- docs/features/graph/pins-in-graph.md
