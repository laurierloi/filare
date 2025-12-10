from: docs/research/termination-diagram-requirements.md

uid: FEAT-TERM-0001
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# Termination Outputs

## Status

PROPOSED

## Priority

Medium

## Summary

Generate termination outputs (CSV/TSV tables and HTML) showing pin/cavity assignments, terminals/seals, strip lengths, tooling, shield/backshell details, and labels/notes. Optional simple connector face diagram later.

## Motivation

Shop-floor and service teams need clear pin tables with prep/tooling to assemble and verify connectors.

## Affected Users / Fields

- Harness manufacturing/QA
- Service/diagnostics

## Scope

- CSV/TSV export with one row per pin/cavity termination.
- HTML table output for human review; optional embedding alongside diagrams.
- Optional connector face diagram (future) showing pin numbering, matched to table.

## Out of Scope

- 3D models; full schematic redraw.

## Requirements

- Pull from `terminations` schema; include connector-level info (family/backshell/shield style).
- Columns for pin/cavity, wire ref/gauge/color, terminal/seal, strip length, tooling, shield prep, notes, labels.
- Optional alternates/pricing if mapped via part model; exclude by default.
- Robust to missing optional fields.

## Steps

- [ ] Implement exporter to CSV/TSV and HTML for termination tables.
- [ ] Add optional face diagram placeholder/hook (future); ensure pin numbering aligns with table.
- [ ] Add CLI flag/output option to generate termination files.
- [ ] Add examples and regression outputs for sealed connectors, shielded terminations, and splices.

## Progress Log

- PROPOSED — termination output generation.

## Validation

- Regression outputs for sample termination YAMLs; verify columns and optional fields; check pin numbering alignment if diagram hook added.

## Dependencies / Risks

- Depends on termination schema; optional face diagram requires pin layout knowledge (could use existing connector pin/pinlabels).
