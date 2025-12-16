# titleblock model
uid: FEAT-RENDER-0011
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: titleblock

## Status

DONE

## Summary

Implement a model for `titleblock.html` and a factory covering title block metadata fields.

## Requirements

- Capture title block fields (pn, company, address, authors, revisions) used by the template.
- Factory should populate required metadata and optional entries (authors/revisions variants).

## Steps

- [x] Identify context keys in `titleblock.html`.
- [x] Define titleblock template model with defaults.
- [x] Add factory_boy factory with author/revision variants.
- [x] Add template tests using factory outputs.

## Progress Log

2025-12-10: Created sub-feature for titleblock template model/factory.
2025-12-11: Implemented faker-backed metadata/options factories plus render tests.

## Sub-Features

- None

## Related Issues

- Parent: docs/features/templates/models.md
