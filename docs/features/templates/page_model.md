from: docs/features/templates/models.md

# Template Model: page

## Status
PLANNED

## Summary
Implement a model for `page.html` and a factory covering page metadata, numbering, and layout flags.

## Requirements
- Capture page metadata (name, index, totals, notes) used by `page.html`.
- Factory should generate page entries with/without optional notes and flags.

## Steps
- [ ] Extract context keys from `page.html`.
- [ ] Define page template model with defaults.
- [ ] Add factory_boy factory with variations in notes/flags.
- [ ] Add template tests using factory outputs.

## Progress Log
2025-12-10: Created sub-feature for page template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
