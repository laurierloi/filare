from: docs/features/graph/parts-and-components-links.md

uid: FEAT-GRAPH-0011
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Parts List Export

## Status

PLANNED

## Summary

Produce a reference parts list (no quantities) by traversing the graph’s Part nodes and their links to components, distinct from the BOM, to enumerate which parts are present in the build.

## Requirements

- Traverse Part nodes and PartLink edges to list unique parts used in the graph; no quantity aggregation (reference-only).
- Keep legacy YAML compatible: parts are derived from existing fields via Part nodes/links.
- Provide a tool/flow to parse config→graph, then emit the parts list export.
- Rendering/BOM remain unchanged; this is an additional export.

## Steps

- [ ] Define the parts list export schema/format.
- [ ] Implement graph traversal to collect unique Part nodes.
- [ ] Add tests/examples and documentation.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created feature spec for a reference-only parts list export from graph traversal.

## Sub-Features

- None

## Related Issues

- docs/features/graph/parts-and-components-links.md
