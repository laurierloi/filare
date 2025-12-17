# termination model

uid: FEAT-RENDER-0010
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: termination

## Status

DONE

## Summary

Implement a model for `termination.html` and a factory to cover termination diagram data via termination_table rendering.

## Requirements

- Capture termination context (rendered termination_table, page metadata/options/titleblock) used by `termination.html`.
- Factory should generate varied termination sets (row counts) and embed rendered table HTML.

## Steps

- [x] Identify context keys in `termination.html`.
- [x] Define termination template model with defaults.
- [x] Add factory_boy factory with termination variations.
- [x] Add template tests using factory outputs.

## Progress Log

2025-12-10: Created sub-feature for termination template model/factory.
2025-12-11: Implemented model + factory rendering termination_table and render tests.

## Sub-Features

- None

## Related Issues

- Parent: docs/features/templates/models.md
