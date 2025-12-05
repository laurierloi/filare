# Cut Diagram Requirements

## Summary

Outlines what a cut diagram (wire/cable cutting instruction) should contain so shop-floor teams can cut and prep harness wires/cables correctly. Focus on fields, annotations, and symbology relevant to Filare.

## Use Cases for Filare

- Generate cut lists/diagrams with lengths, prep, labeling, and material details for manual or automated cutting/printing equipment.
- Provide clear instructions for wires versus multi-conductor cables (bundles), including shielding/termination prep.

## Technical Evaluation

- Core contents:
  - Unique ID per wire/cable segment.
  - Length with units and tolerance; optionally total length vs. cut length (if trim/margin needed).
  - Material reference: cable/wire part number, gauge, color, stranding, jacket/insulation type; for cables: wire count, color map, shield, twist/pairs.
  - End prep per side (Side A/Side B):
    - Strip length, tin/crimp/solder instructions.
    - Terminal type/part number; seal/plug part (if applicable); tooling reference.
    - Shield prep: braid/drain trim length, fold-back, pigtail length, backshell/ground tie note.
    - Boot/heat-shrink/tape instructions at ends.
  - Labels:
    - Label text/ID; position from end (Side A/Side B or center); label type/part; print template reference.
  - Breakouts (for cables):
    - Breakout point distances from a datum (e.g., Side A) and assignment of conductors to branches; prep per branch if applicable.
  - Notes/quality:
    - Special handling (min bend radius, no nicks), torque/strain-relief notes, IPC/WHMA workmanship ref.
- Helpful symbology/format:
  - Table-based cut list with one row per cut item; columns for length, part, color, gauge, prep A/B, labels, notes.
  - Simple line sketch per item (optional) showing length, labels, and end treatments; text annotations usually sufficient.
  - Side identifiers (A/B) clearly mapped to connector/wire IDs in the main harness design.
- Data fields (suggested):
  - `item_id`, `source_design` (cable/wire id), `description`.
  - `length`, `unit`, `tolerance`, optional `extra_allowance`.
  - `part_ref` (wire/cable MPN), `gauge`, `color`, `stranding`, `jacket`, `wire_count/colors` (for cable), `shield` (type).
  - `end_a` / `end_b`: `{strip_length, terminal_pn, seal_pn, tool, shield_prep, boot/shrink/tape, notes}`.
  - `labels`: `{text, position_from_end, side, label_part, template}`.
  - `breakouts`: `{position_from_end, conductors_assigned, prep/label per branch}` (for cables).
  - `quality_notes`, `process_ref` (e.g., IPC/WHMA-A-620 class), `inspection_criteria`.

## Complexity Score (1–5)

2 — Mostly schema and output formatting; no deep render changes if kept as tabular/text instructions.

## Maintenance Risk

- Low; cut instruction formats are stable. Ensure optional fields so minimal datasets still render.

## Industry / Business Usage

- Harness shops use cut sheets/lists to program cutting/strip/tin machines and prepare terminals/seals.
- IPC/WHMA-A-620 workmanship specs often referenced; automotive/aero shops specify strip lengths, shield prep, and labels.

## Who Uses It & Why It Works for Them

- Manufacturing/QA: uses lengths, prep, and tooling to cut/terminate correctly.
- Service: may reference labels and end IDs to replace wires.

## Feasibility

- Feasible to add a cut-list schema and output (CSV/TSV and HTML/PDF) leveraging existing BOM metadata.

## Required Work

- REWORK tasks: Define cut-list data model, tie to existing cables/wires/connectors; ensure optional fields.
- FEATURE tasks: Add cut-list generation and export (CSV/TSV + HTML table), include end prep, labels, breakouts, shield prep.
- DOCUMENTATION tasks: Syntax for cut list; examples; note optional fields and defaults.
- COVERAGE tasks: Regression data for wires and multi-conductor cables with prep/labels/breakouts.

## Recommendation

ADOPT_LATER — Add cut-list schema and outputs; keep rendering simple (tables) with optional line sketches later.
