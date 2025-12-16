# bom model
uid: FEAT-RENDER-0014
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: bom

## Status

DONE

## Summary

Implement a Pydantic model for `bom.html` and a factory_boy factory to generate all field combinations used by the BOM template.

## Requirements

- Model all BOM fields (lines, quantities, units, refs, notes) used in `bom.html`, extending the base template model.
- Factory must emit complete rows and edge cases (missing notes, grouped items, alternates if present).
- Remain compatible with existing BOM rendering expectations.

## Steps

- [x] Identify context keys consumed by `bom.html`.
- [x] Define the BOM template model with typed defaults.
- [x] Add a faker-backed factory with variants covering optional/edge fields.
- [x] Wire into template tests to render BOM with full coverage.

## Progress Log

2025-12-11: Completed BOM template model, factory, and render tests; marking DONE.

## Progress Log

2025-12-10: Created sub-feature for BOM template model/factory.
2025-12-11: Added BomTemplateModel + faker factory and render tests (reverse header variants).

## Command & Testing Notes

- Run targeted suite: `just test-specific tests/templates/test_bom_template_model.py`.
- Factories are faker-backed; capture generated IDs/quantities/descriptions from the model when asserting.
- Cover multiple row counts (e.g., 1/10/50) to ensure layout and header/footer behavior remains correct.

## Sub-Features

- None

## Related Issues

- Parent: docs/features/templates/models.md
