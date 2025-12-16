# images model

uid: FEAT-RENDER-0005
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: images

## Status

DONE

## Summary

Implement a model for `images.html` and a factory to produce image entries with captions and fixed-size variants for testing.

## Requirements

- Capture image fields (src, scale, width, height, fixedsize, caption) used by `images.html`.
- Factory generates images with/without captions and fixed-size variants.

## Steps

- [x] Identify context keys in `images.html`.
- [x] Define images template model with defaults.
- [x] Add factory_boy factory with variants for captions/fixedsize.
- [x] Add template tests using the factory outputs.

## Progress Log

2025-12-10: Created sub-feature for images template model/factory.
2025-12-11: Implemented model + factory (caption/fixed-size variants) and render tests.

## Sub-Features

- None

## Related Issues

- Parent: docs/features/templates/models.md
