from: docs/features/templates/models.md

# Template Model: titleblock

## Status
PLANNED

## Summary
Implement a model for `titleblock.html` and a factory covering title block metadata fields.

## Requirements
- Capture title block fields (pn, company, address, authors, revisions) used by the template.
- Factory should populate required metadata and optional entries (authors/revisions variants).

## Steps
- [ ] Identify context keys in `titleblock.html`.
- [ ] Define titleblock template model with defaults.
- [ ] Add factory_boy factory with author/revision variants.
- [ ] Add template tests using factory outputs.

## Progress Log
2025-12-10: Created sub-feature for titleblock template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
