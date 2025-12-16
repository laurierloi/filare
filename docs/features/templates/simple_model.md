# simple model

uid: FEAT-RENDER-0009
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: simple

## Status

DONE

## Summary

Implement a model for `simple.html` and a factory generating page metadata/content (title, description, diagram, notes, BOM) and container styling.

## Requirements

- Capture fields required by `simple.html` (titles, description, diagram, notes, BOM, container class/style).
- Factory should generate content variants with optional fields and container styling.

## Steps

- [x] Extract context keys from `simple.html`.
- [x] Define simple template model with defaults.
- [x] Add factory_boy factory with optional field variations.
- [x] Add template tests using factory outputs.

## Progress Log

2025-12-10: Created sub-feature for simple template model/factory.
2025-12-11: Implemented model + factory and render tests with container styling.

## Sub-Features

- None

## Related Issues

- Parent: docs/features/templates/models.md
