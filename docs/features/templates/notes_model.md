# notes model
uid: FEAT-RENDER-0018
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: notes

## Status

DONE

## Summary

Implement a model for `notes.html` and a factory to produce notes/annotations lists for testing.

## Requirements

- Capture notes list fields and formatting flags used by `notes.html`.
- Factory should generate multiple notes and empty/omitted cases.

## Steps

- [x] Identify context keys in `notes.html`.
- [x] Define notes template model with defaults.
- [x] Add factory_boy factory with variations in notes content.
- [x] Add template tests using factory outputs.

## Progress Log

2025-12-10: Created sub-feature for notes template model/factory.
2025-12-11: Implemented notes template model/options factory with exhaustive positioning tests; marking DONE.

## Sub-Features

- None

## Related Issues

- Parent: docs/features/templates/models.md
