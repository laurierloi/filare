from: docs/features/templates/models.md

# Template Model: connector

## Status
PLANNED

## Summary
Implement a model for `connector.html` and a factory to cover connector pinouts, labels, sides, and styling flags.

## Requirements
- Capture connector details used by the template (pins, labels, colors, orientation, ports flags).
- Extend base template model where applicable.
- Factory must generate multiple connector shapes/pin layouts for test coverage.

## Steps
- [ ] Identify context keys in `connector.html`.
- [ ] Define connector template model with typed defaults.
- [ ] Add factory_boy factory with variants for pin counts/colors/sides.
- [ ] Add template tests using the factory output.

## Progress Log
2025-12-10: Created sub-feature for connector template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
