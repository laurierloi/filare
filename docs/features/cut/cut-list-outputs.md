from: docs/research/cut-diagram-requirements.md

uid: FEAT-BOM-0002
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# Cut List Outputs

## Status

PROPOSED

## Priority

Medium

## Summary

Generate cut-list outputs (CSV/TSV and HTML tables) from the cut-list schema, including lengths, part references, per-side prep, labels, and breakouts. Optionally include simple line sketches later.

## Motivation

Shop-floor teams need printable/programmatic cut sheets for cutting/strip/tin equipment and QC checks.

## Affected Users / Fields

- Harness manufacturing/QA

## Scope

- CSV/TSV export with one row per cut item.
- HTML table output for human review; optional minimal styling for clarity.
- Include per-side prep, labels, shield prep, and breakout info for cables.

## Out of Scope

- Detailed graphics; machine-specific binary formats.

## Requirements

- Pull from `cut_list` schema; link to existing design IDs for clarity.
- Configurable units display and tolerance.
- Optional inclusion of pricing/part URLs if available from part model/cache.
- Keep outputs optional and separate from main diagram.

## Steps

- [ ] Implement exporter to CSV/TSV and HTML table using cut_list data.
- [ ] Add unit/tolerance formatting and per-side prep columns.
- [ ] Add labels/breakouts/shield prep columns; keep columns optional if data missing.
- [ ] Add CLI flag/output option to generate cut-list files.
- [ ] Add examples and regression outputs for wires and cables.

## Progress Log

- PROPOSED — output generation from cut list.

## Validation

- Regression comparison of CSV/TSV/HTML outputs for sample cut_list YAMLs; verify columns and optional fields.

## Dependencies / Risks

- Depends on cut-list schema; must handle missing optional fields gracefully.
