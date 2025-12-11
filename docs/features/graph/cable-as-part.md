from: docs/features/graph/bundle-model.md

uid: FEAT-GRAPH-0005
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Cable as Part (Graph-Based)

## Status

PLANNED

## Summary

Treat a cable as a part node (FilareModel-backed) that owns metadata (length, shielding, gauge, etc.) and links to its member wires/shields via graph edges, replacing embedded wire objects.

## Requirements

- Represent cables as FilareModel-backed part nodes with UUID4 IDs; defer cable-specific metadata (jacket, impedance, color code) to Part nodes (see parts-and-components-links).
- Link cables to member wires/shields via CableWireLink (same link type for shield or wire) with label/color metadata; remove embedded `wire_objects`.
- Preserve legacy cable YAML by generating member wire/shield nodes and membership links from existing fields; keep rendered outputs/BOM stable.
- Allow cables to participate in bundles via BundleMemberLink; a cable-as-part may be the only element in a bundle.

## Steps

- [ ] Define cable-as-part node fields and membership link payloads.
- [ ] Implement parsing to build cable nodes + member wire/shield links from legacy YAML.
- [ ] Update render/BOM flows to consume graph-backed cable membership; retire embedded wire structures.
- [ ] Add tests/examples for cable graph export and parity with current outputs.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec to treat cables as graph parts with linked member wires/shields.

## Sub-Features

- None

## Related Issues

- docs/features/filare-model-graph-base.md
