# Projection Symbol (First/Third Angle)

uid: FEAT-DOCS-0009
status: BACKLOG
priority: low
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Render projection symbols (first/third angle) per DIN/EN ISO conventions, with metadata to select projection type and show/hide the symbol in title blocks or borders.

## Requirements

- Provide assets/templates for first- and third-angle symbols.
- Metadata flag to select projection type and display location.
- Ensure symbol placement fits DIN framing/title block.

## Steps

- [ ] Add projection metadata key (first/third angle).
- [ ] Insert symbol assets into templates with positioning options.
- [ ] Add regression fixture asserting symbol presence and type in SVG/HTML.

## Progress Log

- 2025-02-20: Feature drafted from DIN research; awaiting implementation.

## Related Issues

- docs/issues/din-projection-symbol.md
- docs/features/mechanical-view-2d.md (projection context for mechanical drawings)
