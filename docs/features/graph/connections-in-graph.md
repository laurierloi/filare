from: docs/features/filare-model-graph-base.md

uid: FEAT-GRAPH-0007
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# Connections in Graph

## Status

PLANNED

## Summary

Move connection logic to FilareLink-based graph edges so pin-to-wire attachments and pin-to-pin loops are tracked in the graph instead of nested on cables/connectors.

## Requirements

- Replace `Connection`/`Loop` storage on cables/connectors with FilareLink subclasses (e.g., PinWireAttachLink, PinLoopLink) referencing pin and wire UUIDs only.
- Support directionality in attachment links (from/to), with an option for undirected if needed; side/label/rendering metadata currently live on the link payload, but we should evaluate separating rendering metadata into dedicated nodes or structures in a follow-up.
- Omit connection role (signal/return) here; other structures can express semantics. One-to-many or many-to-one is modeled by multiple links; termination details (solder/splice/crimp) live on termination links/nodes.
- Preserve legacy YAML (`connections`, `loops`, implicit wiring) by generating link edges from existing fields; emit graph export only when requested.
- Update harness build/render/BOM flows to consume graph-backed connections, keeping outputs stable.

## Steps

- [ ] Design connection link schemas (attach/loop) and payloads for direction/side/metadata.
- [ ] Implement link creation during parsing; adapt to legacy connection definitions.
- [ ] Update harness/render flows to use graph-backed connections; retire `_connections`/loop lists.
- [ ] Add tests/examples for connection graph export and rendering parity; update docs.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec to migrate connections/loops to graph-managed links.

## Sub-Features

- None

## Related Issues

- docs/features/filare-model-graph-base.md
