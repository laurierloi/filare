from: docs/features/filare-model-graph-base.md

uid: FEAT-GRAPH-0010
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# Parts and Components Links

## Status

PLANNED

## Summary

Introduce graph links that associate component instances (connectors, cables, wires, bundles) with purchasable parts, enabling a parts list derived from the graph while keeping component instances separate from their manufactured part definitions.

## Requirements

- Define Part nodes (FilareModel-backed) representing manufactured items (with part numbers, supplier/manufacturer data) stored in the UUID→object map; Part nodes are shared across components (dedup by identifiers).
- Link component nodes (connectors, cables, wires, bundles) to Part nodes via a PartLink (FilareLink subclass) instead of embedding part metadata directly in component instances.
- Preserve legacy part fields (mpn, pn, supplier, etc.) by generating Part nodes and PartLink edges during parsing; keep user-facing YAML compatible.
- Provide a parts list view/export derived from graph traversal (distinct from BOM), aggregating components by linked Part nodes without counting quantities (reference list).
- Keep rendering/BOM outputs stable; part linkage augments data without breaking existing flows; defer richer part attributes to follow-up work.

## Steps

- [ ] Design Part node schema and PartLink payload; map legacy part fields into Part nodes.
- [ ] Implement Part node creation and PartLink generation during parsing; maintain backward compatibility.
- [ ] Add parts list derivation via graph traversal; validate alongside existing BOM.
- [ ] Add tests/examples and documentation for parts list and part linkage export.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec for linking components to manufactured parts and deriving a parts list from the graph.

## Sub-Features

- None

## Related Issues

- docs/features/filare-model-graph-base.md
