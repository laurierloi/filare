from: docs/features/templates/models.md

# Template Model: bom

## Status
PLANNED

## Summary
Implement a Pydantic model for `bom.html` and a factory_boy factory to generate all field combinations used by the BOM template.

## Requirements
- Model all BOM fields (lines, quantities, units, refs, notes) used in `bom.html`, extending the base template model.
- Factory must emit complete rows and edge cases (missing notes, grouped items, alternates if present).
- Remain compatible with existing BOM rendering expectations.

## Steps
- [ ] Identify context keys consumed by `bom.html`.
- [ ] Define the BOM template model with typed defaults.
- [ ] Add a factory_boy factory with variants covering optional/edge fields.
- [ ] Wire into template tests to render BOM with full coverage.

## Progress Log
2025-12-10: Created sub-feature for BOM template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
