from: docs/features/filare-model-graph-base.md
uid: FEAT-GRAPH-0017
status: PLANNED
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Wires in Graph

## Status

PLANNED

## Summary

Refactor wires (and shields) into standalone graph nodes so cables no longer embed wire objects; cable-to-wire membership and pin-to-wire attachments become FilareLink edges in the shared graph.

## Requirements

- Create Wire nodes as FilareModel-backed objects with UUID4 IDs stored in the UUID→object map; cables do not embed `wire_objects`.
- Represent shields as their own node type (e.g., Shield node) with parent metadata; manage shielding via nodes/links rather than embedded fields.
- Connect cables to wires/shields via FilareLink subclasses (e.g., CableWireLink) without relying on link ordering; pin ordering for display comes from pins, not wires.
- Represent twist-pairs via dedicated links (e.g., WirePairLink) between wire nodes.
- Convert pin-to-wire connections into graph links (e.g., PinWireLink) instead of `Cable._connections`; ensure both ends resolve through the UUID→object map.
- Preserve legacy YAML (`wirecount`, `colors`, `wirelabels`, `shield`) by building wire/shield nodes and membership/attachment links from existing fields; emit graph export only when requested.
- Keep BOM/render outputs stable: lengths/gauges/colors handled via graph-backed nodes; impedance/jacket/color can defer to Part linkage (see parts-and-components-links).

## Steps

- [ ] Design Wire/Shield node schema and CableWireLink/PinWireLink payloads (order, label, color, gauge, length).
- [ ] Implement wire node creation and membership/attachment links during parsing; maintain legacy YAML compatibility.
- [ ] Update cable/connection handling and renderers to consume graph-backed wire data; retire `wire_objects`/`_connections` dependencies.
- [ ] Add tests/examples for wire graph export and rendering parity; update docs.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec to move wires/shields into the graph as standalone nodes.

## Sub-Features

- None

## Related Issues

- docs/features/filare-model-graph-base.md
