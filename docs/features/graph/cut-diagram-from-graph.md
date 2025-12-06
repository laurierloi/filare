from: docs/features/graph/bom-from-graph.md

# Cut Diagram from Graph Traversal

## Status

PLANNED

## Summary

Generate cut diagrams by traversing the graph (cable, wire, shield nodes and attachment links) instead of nested structures, aligning with BOM-from-graph for shared data sources.

## Requirements

- Traverse cable/wire/shield nodes and PinWireAttachLink/CableWireLink data to derive cut lengths and labeling (including tolerances and scrap allowances), matching current cut diagram content.
- Keep rendering content the same; ordering may differ if needed, but correctness is priority.
- Provide a tool/flow to parse config→graph, then emit cut diagrams for all harnesses or a subset.
- Use graph-derived data (lengths, colors, labels, tolerances/scrap) and stay compatible with legacy inputs via graph construction.
- Support configurable sorting/grouping (e.g., by bundle, harness, cable, wire) with a default that matches legacy behavior.

## Steps

- [ ] Define traversal and data extraction for cut diagrams using the graph.
- [ ] Implement graph-based cut diagram generation; ensure content parity with current outputs.
- [ ] Add tests/examples and document the flow.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec for cut diagrams via graph traversal.

## Sub-Features

- None

## Related Issues

- docs/features/graph/bom-from-graph.md
