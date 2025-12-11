from: docs/features/templates/models.md

# Template Model: simple-connector

## Status
PLANNED

## Summary
Implement a model for `simple-connector.html` and a factory to cover simplified connector fields/pin labels for testing.

## Requirements
- Capture the simplified connector context (pins/labels/colors) used by `simple-connector.html`.
- Factory should generate pin sets and optional colors/labels combinations.

## Steps
- [ ] Identify context keys in `simple-connector.html`.
- [ ] Define simple-connector model with defaults.
- [ ] Add factory_boy factory with pin/color variations.
- [ ] Add template tests using factory outputs.

## Progress Log
2025-12-10: Created sub-feature for simple-connector template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
