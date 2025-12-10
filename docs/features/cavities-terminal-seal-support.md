from: docs/features/standard-harness-component-support.md
uid: FEAT-GENERAL-0001
status: PROPOSED
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Cavities, Terminals, and Seals Support

## Status

PROPOSED

## Priority

High

## Summary

Add explicit connector cavity definitions with occupancy/population, and attach terminal, seal, and plug part numbers per cavity so BOM and diagrams reflect manufacturing reality instead of generic connectors.

## Motivation

- Automotive and aerospace harness builds require cavity-level part traceability (housing + terminal + seal/plug).
- QC and suppliers validate cavity population against pin tables; missing seals/terminals cause rework and leaks/EMI issues.

## Affected Users / Fields

- Automotive harness engineers and suppliers
- Aerospace/defense wiring teams
- Harness manufacturing/QA

## Scope

- New connector fields to define cavities, occupancy, and per-cavity parts (terminal, seal, plug; optional crimp spec).
- Render cavity tables/metadata in diagrams/HTML; list parts in BOM with correct qty multipliers.
- Backward compatible with existing connectors.

## Out of Scope

- Electrical rule checks beyond presence/absence.
- CAD/PLM import/export.

## Requirements

- Optional `cavities` block on connectors with per-cavity metadata (id/label, populated flag, terminal/seal/plug part refs, notes).
- BOM qty multiplier support for terminals/seals/plugs tied to population count.
- Diagram/HTML display for cavity table (population and part references).
- Ignore-safe: existing connector YAMLs unaffected when fields are absent.

## Steps

- [ ] Design schema additions for connector `cavities` (ids/labels, population, terminal/seal/plug refs, notes).
- [ ] Wire BOM generation to count populated cavities and include terminal/seal/plug parts.
- [ ] Add rendering support for cavity tables with population indicators.
- [ ] Add syntax/docs and examples; regression YAML to cover populated vs unpopulated cavities.
- [ ] Validate BOM/diagram outputs.

## Progress Log

- PROPOSED — sub-feature extracted from standard harness component support.

## Validation

- Regression YAML with a multi-pin connector showing populated/unpopulated cavities, terminal/seal/plug parts in BOM, and cavity table rendering.

## Dependencies / Risks

- Symbol/table layout must fit existing connector rendering style.
- Need clear defaults for population when unspecified (assume populated vs explicit flag).
