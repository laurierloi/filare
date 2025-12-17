# titlepage model

uid: FEAT-RENDER-0012
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: titlepage

## Status

DONE

## Summary

Implement a model for `titlepage.html` and a factory to cover title page metadata, notes, and assets.

## Requirements

- Capture title page fields (name, pn, authors, revisions, logos/notes) used by `titlepage.html`.
- Factory should generate variants with optional logo/notes/authors.

## Steps

- [x] Extract context keys from `titlepage.html`.
- [x] Define titlepage template model with defaults.
- [x] Add factory_boy factory with metadata/logo/note variations.
- [x] Add template tests using factory outputs.

## Progress Log

2025-12-10: Created sub-feature for titlepage template model/factory.
2025-12-11: Added faker-backed page options factory and rendered child templates in tests.

## Sub-Features

- None

## Related Issues

- Parent: docs/features/templates/models.md
