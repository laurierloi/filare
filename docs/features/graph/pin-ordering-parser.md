from: docs/features/graph/pins-in-graph.md
uid: FEAT-GRAPH-0012
status: PLANNED
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Pin Ordering Parser

## Status

PLANNED

## Summary

Provide a graph-based pin ordering parser that derives connector pin orders from pin nodes (and optional interface/grouping metadata) instead of relying on link order, supporting strategies such as low→high, high→low, per-row, or per-interface.

## Requirements

- Derive pin order from pin node metadata (number/index, row/column/interface grouping) without relying on link order.
- Support configurable ordering strategies (low→high, high→low, per-row, per-interface, custom sort keys).
- Keep legacy behavior compatible: default ordering matches current outputs.
- Allow optional export/debug of computed ordering; no change to user-authored YAML by default.

## Steps

- [ ] Define ordering strategy options and required pin node fields (number/index, row/interface tags if available).
- [ ] Implement ordering resolver using the graph/UUID→object map; ensure default matches legacy ordering.
- [ ] Add tests/examples for ordering strategies and parity with current behavior.
- [ ] Document ordering configuration and update feature progress.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec for pin ordering derived from pin node metadata instead of link order.

## Sub-Features

- None

## Related Issues

- docs/features/graph/pins-in-graph.md
