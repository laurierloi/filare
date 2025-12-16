uid: FEAT-RENDER-0004
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: din-6771

## Status
DONE

## Summary
Implement a model for `din-6771.html` and a factory that exercises DIN 6771-specific layout options (notes/BOM toggles, diagram container class/style) and metadata.

## Requirements
- Capture DIN title block fields and layout options used by the template (notes/BOM toggles, bom row sizing, diagram container class/style, title).
- Factory populates required metadata and optional annotations (notes, BOM) and diagram content.

## Steps
- [x] Extract context keys from `din-6771.html`.
- [x] Define din-6771 model with defaults.
- [x] Add factory_boy factory covering required/optional metadata.
- [x] Add template tests using factory outputs.

## Progress Log
2025-12-10: Created sub-feature for din-6771 template model/factory.
2025-12-11: Implemented model + factory with notes/BOM toggles, diagram container styling, and render tests.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
