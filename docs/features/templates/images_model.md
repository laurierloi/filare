from: docs/features/templates/models.md

# Template Model: images

## Status
PLANNED

## Summary
Implement a model for `images.html` and a factory to produce image entries with captions/alt text/links for testing.

## Requirements
- Capture image list fields (path, caption, alt, link) used by `images.html`.
- Factory should generate multiple images and optional fields.

## Steps
- [ ] Identify context keys in `images.html`.
- [ ] Define images template model with defaults.
- [ ] Add factory_boy factory with variants for captions/links.
- [ ] Add template tests using factory outputs.

## Progress Log
2025-12-10: Created sub-feature for images template model/factory.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
