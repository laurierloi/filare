from: docs/features/templates/models.md

# Template Model: cut

## Status
PLANNED

## Summary
Implement a model for `cut.html` and a factory to produce cut diagram inputs (segments, lengths, labels).

## Requirements
- Capture cut diagram fields (segments, labels, distances) used by `cut.html`.
- Factory should produce varied segment lists and optional annotations.

## Steps
- [ ] Extract context keys from `cut.html`.
- [ ] Define cut template model with defaults.
- [ ] Add factory_boy factory with segment/label variations.
- [ ] Add template test using factory outputs.

## Progress Log
2025-12-10: Created sub-feature for cut template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
