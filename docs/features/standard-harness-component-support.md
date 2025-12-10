from: docs/research/harness-diagram-components.md

uid: FEAT-BOM-0007
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


# Standard Harness Component Support

## Status

PROPOSED

## Priority

High (aggregated), with per-component priority in the table below.

## Summary

Add first-class schema and rendering support for the industry-standard harness components called out in the research (cavities, terminals/seals, shield terminations, splices, protection/support/sealing hardware, connector family presets). Today these are only partly representable through generic `additional_components` and notes.

## Motivation

Align Filare diagrams/BOM with common drafting standards (IPC/WHMA-A-620, ISO 6722/19642, USCAR-2, MIL-STD-5088) so suppliers, OEM teams, and service techs see expected callouts and BOM lines without custom post-processing.

## Affected Users / Fields

- Automotive harness engineers (production and service)
- Aerospace/defense wiring teams
- Heavy equipment/industrial harness designers
- Harness manufacturing and QA partners
- Service/diagnostics technicians

## Scope

- New schema fields and rendering symbols for connector cavities, terminal/seal/plug parts, shield termination style/target, explicit splice types, protection devices, sealing/support hardware, and connector family presets with pin maps.
- BOM grouping/sorting that respects new categories.
- Documentation/samples covering the above.

## Out of Scope

- Changes to existing CLI interfaces or breaking schema changes.
- CAD/PLM import/export (can be a future TOOLS follow-up).

## Requirements

- Add explicit component categories instead of overloading `additional_components`.
- Capture cavity occupancy/population and terminal/seal part numbers per connector.
- Capture shield termination metadata (drain target, backshell/pigtail, isolation note).
- Represent splice/junction types as native components.
- Represent protection/sealing/support/label elements as native types that render and appear in BOM with correct multipliers.
- Provide optional connector family presets (e.g., OBD-II, J1939-13, circular/bulkhead families) with default pin labels/maps.
- Keep backward compatibility: existing YAMLs should still work without new fields.

## Priority by Component

- Cavities + terminal/seal/plug parts — High — Automotive/Aero manufacturing and QA.
- Shield termination metadata — High — Aero/defense EMI and automotive shielded lines.
- Splice/junction native types — Medium — Automotive/industrial harness build notes.
- Protection devices (fuse/breaker) — Medium — Service and diagnostics clarity.
- Sealing/support hardware (backshells, boots, clamps, conduit, labels) — Medium — Manufacturing, routing, serviceability.
- Connector family presets — Low — Convenience for rapid authoring and standard interfaces.

## Steps

- [ ] Confirm schema extensions for connectors (cavities, terminal/seal/plug fields) and cables (shield termination metadata) with backward-compatible defaults.
- [ ] Define symbol set additions (splice types, shield drain/backshell, protection devices, support/sealing hardware) for Graphviz/HTML outputs.
- [ ] Extend BOM generation to group/display new component categories and qty multipliers.
- [ ] Add connector family preset definitions and lookup mechanism (OBD-II, J1939-13, circular families).
- [ ] Update docs/syntax and examples to illustrate new fields and symbols; add regression YAMLs.
- [ ] Validate outputs (Graphviz/HTML/BOM) against new examples.

## Progress Log

- PROPOSED — Initial feature request created based on research gaps.

## Validation

- New regression YAMLs covering: (1) connector cavity table with terminal/seal parts, (2) shielded cable with defined termination style/target, (3) splice component rendering, (4) protection + support/sealing hardware in BOM and diagrams, (5) connector preset usage.

## Dependencies / Risks

- Symbol design choices need to align with existing Filare visual style.
- Must avoid breaking existing YAMLs; new fields should be optional and ignore-safe.
- Preset library maintenance requires documented source (standards or OEM pin maps).

## Sub-Features

- cavities-terminal-seal-support
- shield-termination-metadata
