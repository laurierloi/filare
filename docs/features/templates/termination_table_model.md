# termination table model
uid: FEAT-RENDER-0019
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: termination_table

## Status

DONE

## Summary

Implement a model for `termination_table.html` and a factory generating termination table rows with all optional fields.

## Requirements

- Model termination table fields (connector, pin, wire, length, notes) used by the template.
- Factory should emit rows with optional/missing fields to exercise rendering paths.

## Steps

- [ ] Extract context keys from `termination_table.html`.
- [ ] Define termination_table model with defaults.
- [ ] Add factory_boy factory with row variations and edge cases.
- [ ] Add template tests using factory outputs.

## Progress Log

2025-12-10: Created sub-feature for termination_table template model/factory.
2025-12-11: Implemented termination_table model/factory and render tests; marking DONE.

## Sub-Features

- None

## Related Issues

- Parent: docs/features/templates/models.md
