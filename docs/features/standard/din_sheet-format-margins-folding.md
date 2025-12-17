# DIN Sheet Format, Margins, and Folding Marks

uid: FEAT-DOCS-0006
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Align Filare page templates with EN ISO 5457 / DIN 823 for sheet sizes (A0–A4), margins, frames, and folding marks suitable for printing and filing.

## Requirements

- Support DIN/EN ISO sheet sizes with correct margins/frame dimensions.
- Render folding marks for A4 folding.
- Keep existing page sizing configurable without breaking current outputs.
- Provide an example/template demonstrating DIN-compliant framing.

## Steps

- [ ] Add DIN sheet size/margin presets and folding mark rendering to templates.
- [ ] Expose configuration to toggle DIN framing/folding marks.
- [ ] Add regression fixture asserting SVG viewBox/frame dimensions and folding mark coordinates.

## Progress Log

- 2025-02-20: Feature drafted from DIN research; awaiting implementation.

## Related Issues

- docs/issues/din-sheet-format-margins-folding.md
