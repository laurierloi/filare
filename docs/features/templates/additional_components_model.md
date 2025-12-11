from: docs/features/templates/models.md

# Template Model: additional_components

## Status
IN_PROGRESS

## Summary
Implement a Pydantic model for `additional_components.html` (inherits from `template_model.py`) and a factory_boy factory that can populate all template fields for testing coverage.

## Requirements
- Capture all context fields used by `additional_components.html` (including component metadata, counts, and display flags).
- Extend the base template model for shared fields (title/name, output names, etc.).
- Provide a factory_boy factory with defaults and variants for every field combination used in the template.

## Steps
- [x] Map template context variables referenced in `additional_components.html`.
- [x] Define the template model subclass with typed fields/defaults matching the template usage.
- [x] Add a factory_boy-style factory generating complete attribute sets and edge cases (faker-backed with count support).
- [x] Hook the model/factory into template tests to exercise all fields.

## Progress Log
2025-12-10: Created sub-feature plan for additional_components template model/factory.
2025-12-11: Implemented `AdditionalComponentsTemplateModel` + factory and render tests covering id/unit variants and multiple components (faker-backed).
2025-12-11: Added command/testing notes; faker-backed factories generate dynamic IDs/descriptions, so tests should assert against model values, not hard-coded strings.

## Command & Testing Notes
- Run targeted suite: `just test-specific tests/templates/test_additional_components_model.py`.
- Factories are faker-backed; capture generated IDs/quantities/descriptions from the model when asserting.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
