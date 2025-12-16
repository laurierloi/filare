uid: FEAT-RENDER-0017
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: connector

## Status
DONE

## Summary
Implement a model for `connector.html` and a factory to cover connector pinouts, labels, sides, and styling flags.

## Requirements
- Capture connector details used by the template (pins, labels, colors, orientation, ports flags).
- Extend base template model where applicable.
- Factory must generate multiple connector shapes/pin layouts for test coverage.

## Steps
- [x] Identify context keys in `connector.html`.
- [x] Define connector template model with typed defaults.
- [x] Add faker-backed factory with variants for pin counts/colors/sides.
- [x] Add template tests using the factory output.

## Progress Log
2025-12-10: Created sub-feature for connector template model/factory.
2025-12-11: Added `ConnectorTemplateModel` + faker factory and render tests (ports/colors variants, pincount coverage).
2025-12-11: Marked complete with model/factory/tests.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
