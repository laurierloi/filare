from: docs/features/templates/models.md

# Template Model: colors_macro

## Status
PLANNED

## Summary
Implement a model for `colors_macro.html` and a factory ensuring all color/legend combinations are covered for testing.

## Requirements
- Capture color legend entries and display flags used by `colors_macro.html`.
- Factory must produce multiple legend entries and edge cases (empty/omitted).

## Steps
- [ ] Identify context consumed by `colors_macro.html`.
- [ ] Define the colors macro model extending the base template model as needed.
- [ ] Add factory_boy factory with variants for legend richness/empties.
- [ ] Integrate into template tests.

## Progress Log
2025-12-10: Created sub-feature for colors_macro template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
