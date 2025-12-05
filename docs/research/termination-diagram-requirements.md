# Termination Diagram Requirements

## Summary
Defines what termination diagrams/instructions should contain so technicians can terminate wires/cables into connectors/splices correctly. Focus on connector-end prep, seals/plugs, tooling, shield terminations, and labeling in Filare context.

## Use Cases for Filare
- Provide clear instructions for terminating wires/cables to connectors, splices, backshells, and shield ties.
- Support QA and service with explicit pin/cavity assignments and prep steps.

## Technical Evaluation
- Core contents:
  - Component reference: connector/splice ID, family/type, pin/cavity map; for splices, barrel/junction type.
  - Wire/cable references: design IDs, gauge/color, cable conductor ID, shield presence.
  - Pin/cavity assignment table:
    - Pin/cavity ID/label; wire/conductor assigned.
    - Terminal/contacts part number; seal/plug part number (if applicable).
    - Strip length; crimp/solder note; crimp height (optional), insulation support.
    - Tooling: crimp tool, die/locator, extraction tool.
    - Shield termination: backshell tie vs pigtail vs isolated; drain length.
  - Backshell/boot/strain relief:
    - Part numbers; torque/assembly note; order of operations (shield clamp before insertion, etc.).
  - Labels/markers:
    - Label text/ID for connector/branch; placement near connector; flag/heat-shrink part references.
  - Notes/quality:
    - Workmanship spec (IPC/WHMA-A-620), inspection criteria, torque, continuity check.
- Symbology/format:
  - Table of pin assignments with prep columns (strip, terminal, seal, tool).
  - Optional connector face diagram with cavity numbering (especially for multi-pin).
  - Shield tie glyph (ground/backshell) and callouts for boots/strain relief.
  - A/B side references aligned with harness design.
- Data fields (suggested):
  - `connector_id` / `splice_id`, `family/type`, `backshell/boot_pn`, `shield_style`.
  - For each termination (row): `pin_id/label`, `wire_ref`, `wire_gauge/color`, `terminal_pn`, `seal_pn`, `strip_length`, `tool_crimp`, `tool_extract`, `shield_prep`, `note`.
  - Labels: `{text, position, part, template}` near connector.
  - Quality/process: `process_ref`, `torque`, `inspection_notes`.

## Complexity Score (1–5)
3 — Requires schema and output tables, and optional face diagrams for clarity.

## Maintenance Risk
- Low; termination instruction formats are stable; keep optional fields to avoid burden on simple cases.

## Industry / Business Usage
- Harness shops and service manuals show pin tables with strip lengths, terminals/seals, and tooling; shield/backshell instructions are common in automotive/aero/industrial connectors.

## Who Uses It & Why It Works for Them
- Manufacturing/QA: to assemble connectors correctly with correct terminals/seals/tools.
- Service: to re-pin or repair harness ends with clear cavity IDs.

## Feasibility
- Feasible to add termination-list schema and outputs (tables, optional face diagram).

## Required Work
- REWORK tasks: Define termination schema tied to connectors/cables/wires; allow terminals/seals/tooling; shield styles.
- FEATURE tasks: Outputs (CSV/TSV/HTML tables) and optional connector face diagram with pin labels; include labels/notes.
- DOCUMENTATION tasks: Syntax and examples; symbol legend for shield/backshell and pin numbering.
- COVERAGE tasks: Regression YAMLs covering connectors with terminals/seals, shield styles, boots/backshells, and splices.

## Recommendation
ADOPT_LATER — Add termination schema and outputs; start with tables and optional simple face diagram later.
