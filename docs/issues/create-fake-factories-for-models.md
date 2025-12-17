# Issue: Create Fake Factories for Models

uid: ISS-0205
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: 3d
dependencies: []
risk: medium
milestone: backlog

## Status

BACKLOG

## Summary

Add faker-backed factory classes for every model in `src/filare/models/` so tests can generate realistic, varied data without hard-coded literals. Ensure tests are updated to consume these factories rather than constructing models manually.

## Requirements

- Add a `Fake<MODEL>Factory` per model module under `src/filare/models/`, colocated with the model definitions.
- Factories should supply sensible defaults using `faker` and allow overrides for specific fields.
- Update existing tests to build model instances via the new factories.
- Keep factories out of runtime paths (testing/fixtures only).

## Steps

- [ ] Inventory all models under `src/filare/models/` and note missing faker factories.
- [ ] Implement faker factories per model module with override support.
- [ ] Refactor tests to use factories instead of inline model construction.
- [ ] Add targeted `just test-specific` notes/recipes where helpful.
- [ ] Close this issue once all models and tests are covered.

## Progress Log

2025-12-11: Filed issue to track faker factory coverage for all `src/filare/models/` modules and test adoption.

## Related

- docs/features/templates/models.md (faker-backed template factories)
- tests/templates/test_additional_components_model.py
