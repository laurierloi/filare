from: docs/features/templates/models.md

# Template Model: din-6771

## Status
PLANNED

## Summary
Implement a model for `din-6771.html` and a factory that exercises DIN 6771-specific fields and layout options.

## Requirements
- Capture DIN title block fields and layout options used by the template.
- Factory must populate all required metadata fields and optional annotations.

## Steps
- [ ] Extract context keys from `din-6771.html`.
- [ ] Define din-6771 model with defaults.
- [ ] Add factory_boy factory covering required/optional metadata.
- [ ] Add template tests using factory outputs.

## Progress Log
2025-12-10: Created sub-feature for din-6771 template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
