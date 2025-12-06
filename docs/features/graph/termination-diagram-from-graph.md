from: docs/features/graph/bom-from-graph.md

# Termination Diagram from Graph Traversal

## Status

PLANNED

## Summary

Generate termination diagrams by traversing the graph (pins, terminations, wires/shields, attachment links) instead of nested structures, aligning with BOM-from-graph for shared data sources.

## Requirements

- Traverse pins, terminations, wires/shields, and PinTerminationLink/PinWireAttachLink data to derive termination details, matching current termination diagram content.
- Keep rendering content the same; ordering may differ if needed, but correctness is priority.
- Provide a tool/flow to parse config→graph, then emit termination diagrams for all harnesses or a subset.
- Use graph-derived data and stay compatible with legacy inputs via graph construction.

## Steps

- [ ] Define traversal and data extraction for termination diagrams using the graph.
- [ ] Implement graph-based termination diagram generation; ensure content parity with current outputs.
- [ ] Add tests/examples and document the flow.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec for termination diagrams via graph traversal.

## Sub-Features

- None

## Related Issues

- docs/features/graph/bom-from-graph.md
