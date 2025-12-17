# index table model

uid: FEAT-RENDER-0006
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: index_table

## Status

DONE

## Summary

Implement a model for `index_table.html` and a factory generating index rows with PDF variants and layout options.

## Requirements

- Model index entries (items plus PDF-specific items) used by `index_table.html`.
- Factory should produce multiple rows and optional PDF content, and allow layout options (row height, BOM linkage, positioning).

## Steps

- [x] Extract context keys from `index_table.html`.
- [x] Define index_table model with defaults.
- [x] Add factory_boy factory with row variations and PDF items.
- [x] Add template tests using factory outputs.

## Progress Log

2025-12-10: Created sub-feature for index_table template model/factory.
2025-12-11: Implemented model + faker factory with PDF items/layout options and render tests.

## Sub-Features

- None

## Related Issues

- Parent: docs/features/templates/models.md
