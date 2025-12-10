from: docs/features/filare-model-graph-base.md

uid: FEAT-GRAPH-0013
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# Pins in Graph

## Status

PLANNED

## Summary

Refactor pins into standalone graph nodes (FilareModel-backed) so connectors no longer embed pin arrays; pin membership and pin-to-pin loops become FilareLink edges managed in the shared graph.

## Requirements

- Create Pin nodes with UUID4 IDs (FilareModel-backed) stored in the UUID→object map; pins carry their own name/label and pin number/order metadata.
- Connect connectors to pins via FilareLink subclasses (e.g., ConnectorPinLink); connectors only need pin UUIDs and pincount—pin order is held by the pin nodes themselves, so link ordering is not significant.
- Represent loops/bridges between pins as link types (e.g., PinLoopLink) referencing pin UUIDs only.
- Allow pins to link to terminations (splice/crimp/solder/etc.) via dedicated link types; terminations live as graph nodes in their own feature spec.
- Keep existing YAML (`pins`, `pinlabels`, `pincolors`, `loops`) backward compatible: parser builds pin nodes + membership/loop links from legacy fields; emit graph export only when requested.
- Update renderers/BOM to consume graph-derived pins rather than nested connector data, preserving current outputs.

## Steps

- [ ] Design pin node/link schema: Pin node fields, ConnectorPinLink payload (order/side), PinLoopLink payload (side/color/label visibility).
- [ ] Implement Pin node creation and membership/loop links in parsing; maintain legacy YAML compatibility.
- [ ] Update connector models/renderers to resolve pins via graph/UUID→object map instead of nested lists.
- [ ] Add tests/examples covering pin graph export and rendering parity; update docs.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec to move pins into the graph as standalone nodes.

## Sub-Features

- None

## Related Issues

- docs/features/filare-model-graph-base.md
