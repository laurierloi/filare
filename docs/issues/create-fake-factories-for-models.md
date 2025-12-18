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
2025-12-12: Added factories for core models (GraphicalComponentModel/ConnectorModel, CableModel, ComponentModel). Tests updated to consume the new factories and exercise flags (shield/wires/additional/bg) to keep coverage high. Further factories still needed for other models (metadata/options/wire/connection/etc.).
2025-12-13: Converted the new factories to factory_boy + faker and added factories for wire/shield/pin/loop/connection plus metadata/page options. Expanded tests to cover factory variants (colors/bg/partial connections/svg options) and ensure randomized outputs still serialize correctly.
2025-12-14: Added factories for BOM entries, page/document/notes, and harness quantity models with accompanying tests (document manifest/pages, harness quantity defaults, BOM entry variants). Remaining candidates: image/configs/document hash registry utilities and any minor dataclasses not yet covered.

## Related

- docs/features/templates/models.md (faker-backed template factories)
- tests/templates/test_additional_components_model.py
