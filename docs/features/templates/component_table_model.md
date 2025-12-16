# component table model
uid: FEAT-RENDER-0001
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: component_table

## Status

DONE

## Summary

Implement a model for `component_table.html` and a factory generating component payloads with partnumbers, notes, additional components, and image support.

## Requirements

- Model all component table fields (designators, partnumbers, notes, additional components, images) used in the template.
- Factory should emit partnumber list and single-item branches to cover rendering branches.

## Steps

- [x] Extract context keys from `component_table.html`.
- [x] Define component_table model with appropriate defaults.
- [x] Add factory_boy factory generating permutations (notes/images/additional components/partnumber list or single).
- [x] Add tests that render the template using the factory outputs.

## Progress Log

2025-12-10: Created sub-feature for component_table template model/factory.
2025-12-11: Implemented Pydantic model + faker factory with partnumbers/list branch, notes, images, and additional components plus render tests.

## Sub-Features

- None

## Related Issues

- Parent: docs/features/templates/models.md
