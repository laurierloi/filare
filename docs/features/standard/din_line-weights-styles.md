# DIN Line Weights and Styles

uid: FEAT-DOCS-0010
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Parameterize line weights and styles to DIN 15 / EN ISO 128 conventions (visible, hidden, center lines) and ensure rendered SVG/HTML uses configured stroke widths and dash patterns.

## Requirements

- Define default stroke widths/dash patterns per line type.
- Apply styles across rendered elements (borders, objects, annotations).
- Allow overrides while keeping DIN defaults available.

## Steps

- [ ] Add style configuration for DIN line types (visible/hidden/center).
- [ ] Apply styles in renderers/templates.
- [ ] Add regression fixtures checking stroke widths/classes in SVG.

## Progress Log

- 2025-02-20: Feature drafted from DIN research; awaiting implementation.

## Related Issues

- docs/issues/din-line-weights-styles.md
