# Mechanical Harness Diagram Elements and Models

## Summary

Identifies the elements and symbology used in mechanical harness diagrams (nailboard/fixture drawings, routing overlays) and proposes data models to capture geometry, annotations, materials, and hardware. Focus covers dimensions, splicing, shielding, wraps, ties, labels, and correlations between logical and mechanical views.

## Use Cases for Filare

- Generate mechanical overlays for manufacturing (board builds, clamp placement, length checks).
- Provide field/service diagrams with physical routing, labels, and splice/shield details.
- Maintain traceability between electrical nets, BOM items, and mechanical placement.

## Technical Evaluation

- Core elements (mechanical view):
  - Board/fixture outline; datum/grid; reference holes.
  - Harness path polylines with segment lengths, bend radii, breakout points.
  - Features: clamps/tie-downs/edge clips, grommets/bulkheads, pass-throughs, strain relief, boots/backshells.
  - Protective coverings: convolute/conduit, tape wraps, braid, heat-shrink sections with start/end positions.
  - Splices/junctions: inline barrel splices, junction blocks/modules; callouts for splice type and orientation.
  - Shielding: shield drain/termination location; backshell tie vs pigtail vs isolated.
  - Labels/markers: flag labels at breakouts, wire/cable IDs, zone references.
  - Dimensions: overall length, segment lengths, clamp spacing, breakout lengths; tolerance notes.
- Symbols (commonly used):
  - Path: solid polyline with arrows for direction or assembly sequence.
  - Clamps/ties: circles/squares with clamp code; sometimes P-clamp icon; spacing note.
  - Grommet/bulkhead: ring/doorway symbol; callout for hole size and grommet part.
  - Splice: dot for simple inline, or barrel symbol with part number; junction block as rectangle with ports.
  - Shield termination: ground symbol or backshell glyph at connector end; pigtail shown as short branch to ground.
  - Protective coverings: hatched or double-line segments; heat-shrink/tape annotated with start/end distances and part.
  - Labels: flag icon or rectangular tag tied to path; text includes ID and sometimes barcode ref.
  - Dimensions: leader lines with measurement text; chain dimensions along path.
  - Symbol candidates (Unicode-friendly for HTML/SVG legends, with text fallback):
    - Path node: `●` (fallback: "o"); path direction arrow: `➝`.
    - Clamp/tie: `⊙` or `⨀` (fallback: "CL"); P-clamp shorthand: `[C]`.
    - Grommet/bulkhead: `◉` (fallback: "GR").
    - Splice (inline dot): `•`; splice barrel: `▭` with text "SP".
  - Junction block: `▭` with ports; fallback text "JB".
  - Shield to ground: `⏚` (ground) or backshell glyph `⌒`; pigtail branch: short line ending `⏚`.
  - Covering start/end: `▹` / `◃` markers with hatched segment between.
  - Label flag: `⚑` (fallback: "LBL").
  - Dimension: `↔` with text (e.g., `↔ 250 mm`).
- Icon guidance:
  - Prefer self-drawn SVG primitives (circles, rectangles, arcs, hatch patterns) for clamps, splices, junctions, coverings, labels, and dimensions; avoids font licensing and keeps style consistent.
  - Ground/backshell can be drawn with simple shapes mirroring IPC/WHMA/IEC styles (e.g., `⏚`-like ground, arc for backshell).
  - Reference styles (for consistency, not embedding): IPC/WHMA-A-620 nailboard symbols (clamp circles, splice dots/barrels, grommet rings, shield ground at connector). Use them as visual inspiration but render your own SVG.
  - Avoid external icon fonts (Font Awesome/Material) for these domain-specific shapes; they add dependencies and don’t match harness drafting conventions.
- Information captured:
  - Geometry: 2D coordinates in chosen units; orientation of clamps and splice rotation when relevant.
  - Materials: part numbers for clamps, grommets, splices, protective coverings, backshells/boots.
  - Processes: wrap overlap %, tape turns per unit length, heat-shrink recovery note, torque/strain-relief notes.
  - Electrical tie: map mechanical nodes to connector pins/wires/splices for traceability.
  - Environment: notes for temperature/fluids near segments; routing constraints (min bend radius).

## Complexity Score (1–5)

3 — Modeling requires coordinated geometry + materials + annotations but fits within an extended mechanical view without changing electrical core.

## Maintenance Risk

- Symbols and drafting practices are stable (IPC/WHMA-A-620, OEM nailboard guides).
- Risk lies in scope creep if 3D routing or FEA-style checks are attempted; keeping to 2D with optional CAD reference limits churn.
- Optional materials catalogs (clamps, wraps) may need periodic refresh.

## Industry / Business Usage

- Automotive: nailboard drawings with clamp spacing, convolute/tape sections, splice barrels, shield terminations to backshells, label flags at breakouts.
- Aerospace/defense: backshell/boot details, grommets at bulkheads, lacing/tie intervals, shield pigtails or 360° terminations, strain-relief callouts.
- Heavy equipment/industrial: armored/conduit runs, bulkhead glands, vibration-resistant clamps, inline protection devices.

## Who Uses It & Why It Works for Them

- Manufacturing/QA: needs clamp/grommet placements, coverings, and lengths for board setup.
- Service: uses labels, splice locations, and shielding notes to troubleshoot/repair.
- Mechanical/electrical integration: checks pass-throughs, bend radii, and shield terminations against packaging/EMI needs.

## Feasibility

- Feasible with an extended mechanical schema and renderer; symbology can be implemented in SVG/DXF without heavy CAD.

## Fit with Existing Filare Models

- Current fit:
  - Connectors/cables/connections already model electrical nets; `additional_components` can carry clamps/wraps as BOM-only items but lack geometry/placement.
  - `metadata/options` can store drawing-level info but not geometry.
  - Graphviz/HTML renderers are logical-only, so mechanical elements are currently unrendered.
- Gaps: No place for 2D geometry (board outline, paths), feature placement (clamps/grommets/splices), covering intervals, or dimensions. No linkage from mechanical items to nets beyond informal notes.
- Proposed schema additions (compatible path):
  - Add optional top-level `mechanical:` block with: units, datum/grid, outline, reference holes; `paths` with point lists and per-segment metadata; `features` (clamp/tie/grommet/splice/bulkhead/strain-relief) with positions and part refs; `coverings` with start/end distances and material refs; `annotations` for labels/dimensions/notes; `shield_terminations` to locate style/target.
  - Mechanical items reference existing components via IDs (connector, cable, wire, splice id) to correlate mechanical placement to electrical nets/BOM.
  - BOM linkage: features/coverings carry part refs and qty multipliers (length-based or count-based) similar to `additional_components`.
- Alternative implementations:
  - Alt A (inline): Single YAML with `mechanical` block coexisting with existing `connectors/cables`; renderers detect and produce extra SVG/DXF plus HTML embed. Easiest for authors (one file), optional and ignore-safe.
  - Alt B (sidecar): Allow `mechanical:` to accept file refs (include) so large mechanical data can live in a sidecar YAML while core nets stay small. Useful when mechanical data is auto-generated.
  - Alt C (hybrid BOM-only): Keep geometry in an external tool; only attach mechanical part refs as `additional_components` and hyperlink to an external mechanical drawing. Minimal change but loses render integration.
- Renderer integration:
  - New mechanical renderer writes SVG (and optional DXF) alongside existing outputs; HTML includes a tab/section for mechanical view.
  - Symbols table/legend added to HTML for user clarity; defaults chosen to match Filare style.
- User impact:
  - Backward compatibility: existing YAMLs unaffected; `mechanical` is optional.
  - Authoring complexity: adds coordinate entry and feature definitions; mitigated by templates/examples and optional sidecar flow.
  - Output: users gain mechanical SVG/DXF plus legend; may need to learn symbol mapping but aligns with industry nailboard drawings.

## Required Work

- REWORK tasks: Define mechanical entities (path, feature, protective segment, splice, label, dimension) and their relationships to electrical components.
- FEATURE tasks: Add rendering support for symbols (clamp/grommet/splice/shield termination/covering/labels) with distance annotations; support path-based dimensions and breakout markers.
- DOCUMENTATION tasks: Provide a legend of symbols and example mechanical YAML; describe units and datum usage.
- TOOLS tasks: Optional catalogs for clamps/wraps/splices with default symbols; validators for min bend radius and clamp spacing rules.
- COVERAGE tasks: Regression YAMLs covering paths with coverings, clamps, splices, shields, labels, and dimensions.

## Recommendation

ADOPT_LATER — Define the mechanical model first, then implement 2D rendering and validations incrementally.

## Models

- Geometry Model:
  - Units, datum/grid.
  - Board/outline polygon; reference holes.
  - Path polylines with points, segment metadata (length, bend radius, covering refs).
  - Breakouts: path nodes marking where bundles split; mapping to connector/wire groups.
- Feature Model:
  - Clamps/ties/edge clips: type, position, orientation, part ref, spacing rule.
  - Grommets/bulkheads: position, opening size, part ref, pass-through link to path.
  - Strain relief/boots/backshells: association to connector end; part refs.
  - Splices/junctions: position, splice type, part ref, involved wires/nets; orientation optional.
- Covering Model:
  - Segments referencing path intervals with material (conduit, braid, tape, heat-shrink), start/end distances, overlap %, color, part ref.
  - Shield termination: end association, style (backshell/pigtail/isolated), hardware ref.
- Annotation Model:
  - Labels/markers tied to path positions or features; text, ID, optional barcode ref.
  - Dimensions: chain/ordinate along path, clamp spacing, breakout lengths; tolerance.
  - Notes: process notes (tape turns per unit, shrink temp), environment notes.
- Correlations:
  - Path nodes ↔ connectors/cables/wires to trace mechanical to electrical.
  - Feature/covering parts ↔ BOM items and to-wire counts (e.g., qty multiplier by terminations or segment length).
  - Shield termination ↔ connector/ground point and BOM backshell/ground hardware.

## References

- IPC/WHMA-A-620 (workmanship and harness drawings)
- OEM nailboard/fixture drafting guides (automotive, aerospace)
- Common CAD/CAM nailboard outputs (DXF) used in harness shops

## Optional Appendix

- Symbol legend candidates: polyline path; P-clamp icon; grommet ring; splice dot/barrel; shield ground/backshell glyph; hatched covering; tape/heat-shrink start-end ticks; flag label; chain dimensions along path.
