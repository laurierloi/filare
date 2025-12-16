# cut model

uid: FEAT-RENDER-0003
status: DONE
priority: medium
owner_role: FEATURE
estimate: 1d
dependencies: []
risk: medium
milestone: templates-models

from: docs/features/templates/models.md

# Template Model: cut

## Status

DONE

## Summary

Implement a model for `cut.html` and a factory to produce cut diagram inputs that render the cut table and page metadata.

## Requirements

- Capture cut diagram fields (rendered cut_table HTML, page metadata/options/titleblock).
- Factory produces varied cut_table row counts via the cut_table factory.

## Steps

- [x] Extract context keys from `cut.html`.
- [x] Define cut template model with defaults.
- [x] Add factory_boy factory with cut_table variations.
- [x] Add template test using factory outputs.

## Progress Log

2025-12-10: Created sub-feature for cut template model/factory.
2025-12-11: Implemented model + factory rendering cut_table HTML and render tests.

## Sub-Features

- None

## Related Issues

- Parent: docs/features/templates/models.md
