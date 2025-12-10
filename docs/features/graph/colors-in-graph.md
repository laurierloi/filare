from: docs/features/filare-model-graph-base.md

uid: FEAT-GRAPH-0006
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# Colors in Graph

## Status

PLANNED

## Summary

Represent colors as reusable graph nodes so connectors, pins, wires, and cables link to shared color objects instead of embedding color payloads, reducing duplication and simplifying color inheritance.

## Requirements

- Create Color nodes (FilareModel-backed) with UUID4 IDs stored in the UUID→object map; capture both identification role (user-facing palette) and physical/color-code role (actual wire/cable color) as attributes, including color codes.
- Link components (connectors, pins, wires, cables) to colors via FilareLink subclasses (e.g., ColorLink) with distinct roles (body/bg/pin/jacket/etc.) to disambiguate usage; reuse color nodes across components is allowed/encouraged.
- Preserve legacy YAML color fields (strings, lists, color codes): parser generates Color nodes and link edges from existing values; emit graph export only when requested.
- Ensure color inheritance/overrides (e.g., cable color palettes, pincolors, Belden codes) resolve through color nodes without changing rendered output; support palette changes (e.g., grayscale) by updating color nodes.

## Steps

- [ ] Design Color node schema and ColorLink payload (role/slot to differentiate body/background/pin colors).
- [ ] Implement Color node creation and linking during parsing; honor legacy color parsing paths.
- [ ] Update renderers to resolve colors via graph/UUID→object map while keeping output identical.
- [ ] Add tests/examples validating color graph export and rendering parity; update docs.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec to move colors into the graph as reusable nodes.

## Sub-Features

- None

## Related Issues

- docs/features/filare-model-graph-base.md
