from: docs/features/filare-model-graph-base.md

uid: FEAT-GRAPH-0008
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Connector–Cable–Connector in Graph

## Status

PLANNED

## Summary

Model end-to-end connector↔cable↔connector relationships as graph edges, replacing implicit connection storage with FilareLink-based attachments between connector pins and cable wire nodes.

## Requirements

- Use Pin nodes (from pins-in-graph) and Wire/Shield nodes (from wires-in-graph) to represent endpoints; connectors and cables stay linkless aside from their UUIDs.
- Define link types for attachment: ConnectorPinLink (connector→pin), CableWireLink (cable→wire/shield, same link type for wire or shield), and PinWireAttachLink (pin→wire) to capture the full connector–cable–connector chain via UUIDs.
- Preserve directionality metadata where needed for rendering/BOM; link order is not significant because pin ordering is on the pin node. Outputs remain backward compatible with current diagrams and quantity calculations.
- Keep legacy YAML (`connections`, `wirelabels`, `colors`, etc.) working by generating the same attachment links during parsing; expose a graph export for debug only.
- Candidate link payload fields (to be finalized): direction (from/to), optional signal label/alias, optional termination reference (uuid), optional render hints (may move to render-metadata-separation).

## Steps

- [ ] Design attachment link payloads to capture endpoint roles (from/to), order, and rendering hints.
- [ ] Implement attachment link creation during parsing; map legacy connection constructs to graph links.
- [ ] Update render/BOM flows to resolve connector↔cable↔connector chains via graph traversal.
- [ ] Add tests/examples and documentation for the graph-based attachment model.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec for connector–cable–connector attachment via graph links.

## Sub-Features

- None

## Related Issues

- docs/features/filare-model-graph-base.md
