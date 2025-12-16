# colors macro model
uid: FEAT-RENDER-0016
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: colors_macro

## Status

DONE

## Summary

Implement a model for `colors_macro.html` and a factory ensuring all color/legend combinations are covered for testing.

## Requirements

- Capture color legend entries and display flags used by `colors_macro.html`.
- Factory must produce multiple legend entries and edge cases (empty/omitted).

## Steps

- [x] Identify context consumed by `colors_macro.html`.
- [x] Define the colors macro model extending the base template model as needed.
- [x] Add a faker-backed factory with variants for legend richness/empties.
- [x] Integrate into template tests.

## Progress Log

2025-12-10: Created sub-feature for colors_macro template model/factory.
2025-12-11: Added ColorsMacroTemplateModel + faker factory and render tests (count variants).
2025-12-11: Marked complete with model/factory/tests.

## Sub-Features

- None

## Related Issues

- Parent: docs/features/templates/models.md
