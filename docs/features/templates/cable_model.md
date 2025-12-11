from: docs/features/templates/models.md

# Template Model: cable

## Status
PLANNED

## Summary
Implement a model for `cable.html` and a factory covering all cable-specific attributes (wire counts, labels, colors, lengths).

## Requirements
- Extend base template model with cable fields used by `cable.html` (wires, shields, labeling, lengths).
- Factory should generate combinations for wires/shields/colors to exercise rendering branches.

## Steps
- [ ] Extract context keys from `cable.html`.
- [ ] Define cable template model with defaults.
- [ ] Add factory_boy factory with variants for wires/shields/colors.
- [ ] Add tests rendering cable template using factory outputs.

## Progress Log
2025-12-10: Created sub-feature for cable template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
