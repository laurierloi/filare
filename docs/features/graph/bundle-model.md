from: docs/features/filare-model-graph-base.md

# Bundle Model in Graph

## Status

PLANNED

## Summary

Define a Bundle as a FilareModel-backed node representing an ensemble of wires/cables, with membership expressed via graph links instead of nested structures.

## Requirements

- Create a Bundle node type (FilareModel-backed) with UUID4 ID in the UUID→object map; captures bundle metadata (name/type/category) and mechanical details.
- Link bundles to member wires/cables via FilareLink subclasses (e.g., BundleMemberLink) carrying label/slot metadata when needed; bundles may nest (bundle→bundle) to represent harness hierarchy.
- Support mechanical details via links to tie information (how the bundle is kept together), labels (identification), and sheathing (type of sheath used).
- Preserve legacy bundle representations (e.g., cable category=bundle) by building bundle nodes and membership links from existing YAML; keep outputs backward compatible.
- Allow partial wire membership (e.g., only first 2/3 of a wire in one bundle, remaining in another) via link payloads or segment metadata.
- Ensure render/BOM flows can resolve bundle membership via graph traversal without relying on nested wire lists.
- Note: Bundles can be nested; a harness can be viewed as connector→bundles→bundles→bundles→connectors at the highest level.

## Steps

- [ ] Design Bundle node schema, membership link payloads (including partial/segment metadata), and mechanical links (ties/labels/sheathing).
- [ ] Implement bundle node creation and member links in parsing; adapt legacy bundle YAML and support bundle nesting.
- [ ] Update render/BOM flows to use graph-backed bundles.
- [ ] Add tests/examples for bundle graph export and parity with current outputs.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec for bundle nodes and membership links.

## Sub-Features

- None

## Related Issues

- docs/features/filare-model-graph-base.md
