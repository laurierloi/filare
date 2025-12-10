from: docs/features/filare-model-graph-base.md

uid: FEAT-GRAPH-0003
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# BOM from Graph Traversal

## Status

PLANNED

## Summary

Generate BOM entries by traversing the graph of nodes/links (connectors, cables, wires, shields, bundles, parts) instead of relying on nested model structures, ensuring a single source of truth for quantities and relationships.

## Requirements

- Define traversal rules over the UUID→object map and graph links to produce BOM entries for connectors, cables, wires, shields, bundles, and additional components; prefer Part linkage when present, fall back to component fields otherwise.
- Ensure per-harness quantity multipliers, lengths, and categories are derived from graph data (e.g., wire lengths on PinWireAttachLink/CableWireLink).
- Preserve existing BOM output shape/content; ordering is less critical than correctness.
- Provide a tool/flow to parse config→graph, then generate BOM from the graph for all harnesses or a subset.
- Support optional graph export/debug flows to validate BOM derivation without requiring user-authored graph data.

## Steps

- [ ] Design traversal strategy and link/node roles needed for BOM derivation (categories, multipliers, lengths).
- [ ] Implement BOM builder atop the graph; map outputs to existing BOM models.
- [ ] Add tests/examples comparing legacy BOM generation vs graph-derived BOM for parity.
- [ ] Document the traversal approach and update feature progress.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec for BOM generation via graph traversal.

## Sub-Features

- None

## Related Issues

- docs/features/graph/cut-diagram-from-graph.md
- docs/features/graph/termination-diagram-from-graph.md
- docs/features/filare-model-graph-base.md
