# cut table model

uid: FEAT-RENDER-0002
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: cut_table

## Status

DONE

## Summary

Implement a model for `cut_table.html` and a factory covering cut-list table rows (wire, part number, color, length) with color modeling.

## Requirements

- Model all cut table fields (wire name, part number, color, length) used by `cut_table.html`.
- Factory emits varied row counts with typed SingleColor values.

## Steps

- [x] Identify context keys in `cut_table.html`.
- [x] Define cut_table model with typed defaults.
- [x] Add factory_boy factory with row variants.
- [x] Add template tests using the factory outputs.

## Progress Log

2025-12-10: Created sub-feature for cut_table template model/factory.
2025-12-11: Implemented model + faker factory with typed colors and render tests.

## Sub-Features

- None

## Related Issues

- Parent: docs/features/templates/models.md
