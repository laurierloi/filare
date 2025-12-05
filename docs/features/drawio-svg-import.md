# DrawIO SVG Import

## Status

DONE

## Summary

Allow Filare to import an arbitrary SVG exported from DrawIO and embed it into rendered pages so DrawIO diagrams can appear alongside generated wiring outputs.

## Requirements

- Accept user-supplied SVG files exported from DrawIO without requiring manual edits.
- Provide configuration to place the SVG on a page with controllable size/position so it aligns with other Filare content.
- Preserve original DrawIO styling (fonts, colors, layers) while allowing optional scaling to fit Filare page bounds.
- Work across HTML and SVG outputs (and PDF if generated via the SVG/HTML pipeline) without breaking existing render flows.
- Document how to supply the SVG and specify its placement.

## Steps

- [x] Define YAML schema additions for referencing external DrawIO-exported SVG assets at the page level.
- [x] Implement renderer support to load, scale, and position the imported SVG within Filare page outputs while retaining styling.
- [x] Add regression coverage and docs/examples showing a DrawIO SVG embedded in a page.

## Progress Log

2025-12-04: Created feature request, captured requirements, and waiting for operator review before implementation.
2025-12-04: Added follow-up sub-feature request for deeper DrawIO authoring integration.
2025-12-04: Status set to IN_PROGRESS after operator approval; starting implementation planning.
2025-12-04: Added diagram_svg schema, rendering pipeline support, tests, and docs for embedding DrawIO-exported SVGs; ran uv run pytest tests/features/drawio-svg-import tests/render/test_assets.py tests/render/test_html_generation.py.
2025-12-04: Improved PNG handling (skip when importing SVG), added DrawIO demo example, expanded path resolution, added viewBox/root checks, ensured templates work, and added tests for coverage.

## Sub-Features

- drawio-integration

## Related Issues

- None.
