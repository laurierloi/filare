uid: FEAT-RENDER-0015
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: cable

## Status
DONE

## Summary
Implement a model for `cable.html` and a factory covering all cable-specific attributes (wire counts, labels, colors, lengths).

## Requirements
- Extend base template model with cable fields used by `cable.html` (wires, shields, labeling, lengths).
- Factory should generate combinations for wires/shields/colors to exercise rendering branches.

## Steps
- [x] Extract context keys from `cable.html`.
- [x] Define cable template model with defaults.
- [x] Add a faker-backed factory with variants for wires/shields/colors.
- [x] Add tests rendering cable template using factory outputs.

## Progress Log
2025-12-10: Created sub-feature for cable template model/factory.
2025-12-11: Added CableTemplateModel + faker factory and render tests (wirecount/shield variants).
2025-12-11: Marked complete with all tests and factories in place.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
