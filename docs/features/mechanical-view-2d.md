from: docs/research/mechanical-harness-diagrams.md

uid: FEAT-MECH-0002
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# 2D Mechanical Harness View (SVG/DXF)

## Status

PROPOSED

## Priority

Medium

## Summary

Add a lightweight 2D mechanical view showing harness routing on a board/fixture: outlines, datum grid, clamps/tie-downs/grommets, pass-throughs, and path polylines with lengths. Export as SVG (embedded in HTML) and optionally DXF for manufacturing.

## Motivation

- Board builds and QA need clamp locations, path lengths, and datum references.
- Mechanical/electrical integration benefits from a simple routing overlay without requiring CAD.

## Affected Users / Fields

- Harness manufacturing/QA teams
- Mechanical/electrical integration teams
- Service technicians needing layout context

## Scope

- New schema block for mechanical view: units, board outline, datum/grid, features (holes, clamps, grommets), and harness path polylines with segment lengths.
- Render to SVG (always) and DXF (optional) alongside existing outputs; embed SVG in HTML output.

## Out of Scope

- 3D routing or clearance analysis.
- Direct CAD ingestion (handled in separate feature).

## Requirements

- Mechanical schema that is ignore-safe when absent.
- SVG renderer for board outline, features, labels, and path with length callouts.
- Optional DXF export for shop use.
- Integration with existing output flow (write alongside other outputs; link from HTML).

## Steps

- [ ] Define `mechanical` YAML schema block (units, outline, features, paths, labels).
- [ ] Implement SVG generator for mechanical view; embed in HTML output.
- [ ] Add optional DXF exporter (ezdxf) gated behind dependency check.
- [ ] Add examples and regression YAML for mechanical view.
- [ ] Update docs/syntax with mechanical block and outputs.

## Progress Log

- PROPOSED — created from mechanical harness research.

## Validation

- Regression YAML that renders mechanical SVG and (when enabled) DXF; verify paths, feature markers, and length callouts.

## Dependencies / Risks

- Keep DXF dependency optional to avoid bloating installs.
- Coordinate system/units must be documented to avoid mis-scaled outputs.
