from: docs/features/templates/models.md

# Template Model: index_table

## Status
PLANNED

## Summary
Implement a model for `index_table.html` and a factory generating index rows with links/notes/qty flags for testing.

## Requirements
- Model index entries (page name, link, notes, qty flags) used by `index_table.html`.
- Factory should produce multiple rows and optional content fields.

## Steps
- [ ] Extract context keys from `index_table.html`.
- [ ] Define index_table model with defaults.
- [ ] Add factory_boy factory with row variations and optional notes.
- [ ] Add template tests using factory outputs.

## Progress Log
2025-12-10: Created sub-feature for index_table template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
