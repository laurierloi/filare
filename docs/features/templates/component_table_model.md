from: docs/features/templates/models.md

# Template Model: component_table

## Status
PLANNED

## Summary
Implement a model for `component_table.html` and a factory generating table rows with all component fields exercised.

## Requirements
- Model all component table fields (designators, refs, descriptions, notes) used in the template.
- Factory should emit multiple rows and optional fields to cover rendering branches.

## Steps
- [ ] Extract context keys from `component_table.html`.
- [ ] Define component_table model with appropriate defaults.
- [ ] Add factory_boy factory generating row combinations and edge cases.
- [ ] Add tests that render the template using the factory outputs.

## Progress Log
2025-12-10: Created sub-feature for component_table template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
