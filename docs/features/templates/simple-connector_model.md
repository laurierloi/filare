uid: FEAT-RENDER-0008
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: simple-connector

## Status
DONE

## Summary
Implement a model for `simple-connector.html` and a factory to cover simplified connector fields/pin labels/colors for testing.

## Requirements
- Capture the simplified connector context (pins/labels/colors, subtype, pincount) used by `simple-connector.html`.
- Factory generates pin sets with optional color bar.

## Steps
- [x] Identify context keys in `simple-connector.html`.
- [x] Define simple-connector model with defaults.
- [x] Add factory_boy factory with pin/color variations.
- [x] Add template tests using factory outputs.

## Progress Log
2025-12-10: Created sub-feature for simple-connector template model/factory.
2025-12-11: Implemented model + faker factory (color on/off) and render tests.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
