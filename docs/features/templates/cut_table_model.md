from: docs/features/templates/models.md

# Template Model: cut_table

## Status
PLANNED

## Summary
Implement a model for `cut_table.html` and a factory covering cut-list table rows and optional fields.

## Requirements
- Model all cut table fields (wire name, lengths, prep info) used by `cut_table.html`.
- Factory must emit rows with and without optional fields to cover branches.

## Steps
- [ ] Identify context keys in `cut_table.html`.
- [ ] Define cut_table model with typed defaults.
- [ ] Add factory_boy factory with row variants and edge cases.
- [ ] Add template tests using the factory outputs.

## Progress Log
2025-12-10: Created sub-feature for cut_table template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
