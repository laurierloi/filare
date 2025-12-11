from: docs/features/templates/models.md

# Template Model: termination

## Status
PLANNED

## Summary
Implement a model for `termination.html` and a factory to cover termination diagram data (pins, terminations, notes).

## Requirements
- Capture termination context (pins, labels, hardware) used by `termination.html`.
- Factory should generate varied termination sets and optional notes.

## Steps
- [ ] Identify context keys in `termination.html`.
- [ ] Define termination template model with defaults.
- [ ] Add factory_boy factory with termination variations.
- [ ] Add template tests using factory outputs.

## Progress Log
2025-12-10: Created sub-feature for termination template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
