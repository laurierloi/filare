from: docs/research/cut-diagram-requirements.md

uid: FEAT-BOM-0004
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Cut List Template

## Status

PROPOSED

## Priority

Medium

## Summary

Define a configurable cut-list template (column layout, formatting, optional symbols) for CSV/TSV/HTML exports, so teams can tailor the cut sheet to their process while keeping required fields consistent (lengths, prep per side, labels, breakouts).

## Motivation

Manufacturing and QA often need specific columns/order, unit formatting, and label/prep visibility to align with their cutters, printers, or QC checklists.

## Affected Users / Fields

- Harness manufacturing/QA
- Service (when reviewing printed cut sheets)

## Scope

- Template definition for cut-list outputs: column selection/order, unit display, tolerance display, per-side prep formatting, label position formatting, optional notes inclusion.
- HTML styling hooks and CSV/TSV column defaults with overrides.

## Out of Scope

- Machine-specific proprietary formats.
- Graphical line sketches (separate feature if needed).

## Requirements

- Default template with required columns: item_id, source (wire/cable), length+unit+tolerance, part/mpn, gauge/color, end A prep, end B prep.
- Optional columns toggles: labels (text/position/part), shield prep, breakouts, notes, process refs.
- Unit/tolerance formatting options; per-side prep formatting (strip length, terminal/seal/tool, shield prep).
- HTML template supports basic styling (row striping, column visibility) via config; CSV/TSV honor column order.
- Keep templates optional; fall back to default layout if none provided.

## Steps

- [ ] Define template config schema (columns list with keys/labels/format rules; per-field format options for units, tolerances, prep).
- [ ] Provide default templates (full; compact) and allow overrides via CLI/config.
- [ ] Implement template application in cut-list exporters (CSV/TSV/HTML).
- [ ] Document template usage with examples.
- [ ] Add regression outputs showing default vs custom template application.

## Progress Log

- PROPOSED — template specification for cut-list outputs.

## Validation

- Regression outputs for sample cut_list data with default and custom templates; verify column order, visibility, and formatting.

## Dependencies / Risks

- Depends on cut-list schema and output generation; must handle missing optional fields gracefully.
