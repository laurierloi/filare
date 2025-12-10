from: docs/research/termination-diagram-requirements.md

uid: FEAT-TERM-0003
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# Termination Template

## Status

PROPOSED

## Priority

Medium

## Summary

Define a configurable template for termination outputs (CSV/TSV/HTML) to control column selection/order and formatting (units, strip length formatting, per-pin tooling visibility), while keeping required pin/cavity info consistent.

## Motivation

Manufacturing/QA often need specific column layouts and visibility (e.g., show seal/plug columns for sealed connectors, hide tooling when not used); service may want simplified views.

## Affected Users / Fields

- Harness manufacturing/QA
- Service/diagnostics

## Scope

- Template config for columns/labels/order; unit/format options for strip lengths; optional columns toggles (seal, tool, shield prep, notes).
- HTML styling hooks (visibility, striping) and CSV/TSV column ordering.

## Out of Scope

- Connector face graphics (handled separately if added).

## Requirements

- Default template with required columns: connector/splice id, pin/cavity, wire ref, terminal, strip length.
- Optional columns toggles: seal/plug, tool_crimp/tool_extract, shield_prep, backshell/boot, labels, notes/process refs, gauge/color.
- Unit formatting for strip lengths; allow hiding empty columns.
- Templates optional; fall back to default if none provided.

## Steps

- [ ] Define template config schema (columns list with keys/labels/format rules; unit formatting for strip lengths).
- [ ] Provide default templates (full vs compact) and allow overrides via CLI/config.
- [ ] Apply template in termination exporters (CSV/TSV/HTML).
- [ ] Document usage with examples.
- [ ] Add regression outputs showing default vs custom templates.

## Progress Log

- PROPOSED — template specification for termination outputs.

## Validation

- Regression outputs for sample termination data with default and custom templates; verify column order/visibility/formatting.

## Dependencies / Risks

- Depends on termination schema and output generation; must handle missing optional fields cleanly.
