uid: FEAT-RENDER-0007
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: page

## Status
DONE

## Summary
Implement a model for `page.html` and a factory covering page metadata, options (font/bg/titleblock rows), and titleblock content.

## Requirements
- Capture page metadata (generator/title/template sizing) and styling options used by `page.html`.
- Factory should generate page entries with configurable options/titleblock snippets.

## Steps
- [x] Extract context keys from `page.html`.
- [x] Define page template model with defaults.
- [x] Add factory_boy factory with variations in options/metadata.
- [x] Add template tests using factory outputs.

## Progress Log
2025-12-10: Created sub-feature for page template model/factory.
2025-12-11: Implemented model + faker factory using shared page metadata/options factories and render tests.

## Sub-Features
- None

## Related Issues
- Parent: docs/features/templates/models.md
