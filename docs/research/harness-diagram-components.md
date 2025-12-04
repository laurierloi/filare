# Standard Harness Diagram Components

## Summary
Survey of the component types that appear most often in industry harness diagrams (automotive, aerospace, industrial equipment). The goal is to ensure Filare can represent the canonical parts, metadata, and symbology that engineers expect when reading or generating harness drawings.

## Use Cases for Filare
- Authoring harness diagrams that match OEM and supplier drawing conventions.
- Generating BOMs that map directly to connector housings, terminals, seals, splices, and protection hardware.
- Validating completeness (grounds, shielding termination, strain relief) during design reviews.
- Exchanging data with CAD/PLM systems that expect standard component classes.

## Technical Evaluation
- Features: Connectors (housings, pins, cavities, gender, keying), wires/cables (gauge, color, insulation, shielding, twisting), splices and junctions, ground points, inline protection (fuses, breakers), termination hardware (backshells, boots, strain relief), sealing (grommets, gaskets, cavity plugs), protective coverings (conduit, braid, tape, heat-shrink), mechanical supports (clips, clamps, tie-downs), labels/ID markers, test points, inline devices (resistors/diodes for sense lines), bulkhead and pass-through hardware, reference datums for harness boards.
- Strengths: Widely adopted across IPC/WHMA-A-620, ISO 6722/19642, USCAR-2, SAE J1939-13/J1962, MIL-STD-5088, and OEM drafting guides; clear mapping to BOM line items; consistent symbols (connector rectangle with pin table, splice dot or barrel symbol, shield drains, ground lug).
- Weaknesses: Symbol sets vary slightly by industry (aerospace vs automotive); some vendors add proprietary codes for cavities/seals; shield representation differs between single-core and multi-core cables.
- Limitations: Environmental details (temperature class, fluid exposure) often live in notes rather than symbols; strain relief and boots may be depicted textually; braid/conduit coverage percentages rarely shown graphically.
- Compatibility with Filare: Fits existing notion of components and nets but would benefit from explicit types for connectors, splices, grounds, shields, protection, sealing, and support hardware. Symbology could map to Graphviz/HTML layers; BOM already accommodates extra metadata.
- Required integrations: Schema fields for cavity definitions, terminal/crimp spec, seal/plug part numbers, shield termination style, strain relief/backshell references, wire dress (twist, bundle, breakout), and mounting hardware callouts.

## Complexity Score (1–5)
3 — Adds structured component categories and attributes beyond current generic parts. Requires schema extensions (cavities, sealing, shield termination), updated render symbols, and BOM grouping, but does not require deep architectural changes.

## Maintenance Risk
- External tool stability: Standards are mature and slow-changing (IPC/WHMA, ISO 6722/19642, USCAR-2, MIL-STD-5088). Low risk of churn.
- Ecosystem health: Strong vendor support (TE, Molex, Aptiv, Amphenol, Deutsch), and PLM/CAD suites model the same component classes.
- Filare-side work: Maintaining symbol set, schema mappings, and reference metadata tables; occasional updates when OEM drafting guides change.
- Expected ongoing cost: Low to moderate; mainly keeping part-type dictionaries and render icons aligned with new connectors/seals.

## Industry / Business Usage
- Automotive harness drawings: Connector housings with cavity tables, terminal/plug/seal callouts, splice barrels, shield drains, ground lugs, convolute tubing and tape wraps, P-clamps/edge clips, and labels at breakouts.
- Aerospace/defense: Circular connectors with backshells and environmental sealing, shield termination to backshell or pigtail, grounding studs, lacing/tie wraps, strain relief boots, in-line splices and junction modules per MIL-STD-5088.
- Heavy equipment/industrial: Bulkhead feedthroughs, gland plates, armored cable, inline fuses/breakers, conduit, and clamp spacing notes for vibration control.
- Service diagnostics: Standard interface connectors (SAE J1962 OBD-II, SAE J1939-13) with pin assignments and protective caps.

## Who Uses It & Why It Works for Them
- OEM harness teams (automotive and heavy equipment): Ensures suppliers can build and QC harnesses from standardized symbols; aligns BOM with procurement catalogs.
- Aerospace integrators: Depend on explicit backshell/shield/strain-relief callouts for EMI and environmental sealing compliance.
- Service and diagnostics teams: Need recognizable connector symbols with cavity numbering for probing and repair.
- Harness manufacturing partners: Use splice/terminal/seal detail to set up crimping, sealing, and over-mold processes.

## Feasibility
- Feasible now with schema and renderer extensions; no external dependencies beyond expanding component dictionaries and symbols.

## Required Work
- REWORK tasks: Align component taxonomy (connectors, splices, protection, sealing, support) and ensure BOM grouping/sorting can handle new categories.
- FEATURE tasks: Add schema fields for cavities, terminal/seal/plug parts, shield termination style, backshell/boot/strain relief references, protective coverings, and clamp/label definitions; add standard symbols for splices, shield drains, grounds, protective devices, and support hardware; support connector families (OBD-II, J1939-13, circular, micro-fit, etc.).
- DOCUMENTATION tasks: Update syntax docs with component categories and examples; provide symbol legend and drafting notes aligned with IPC/WHMA and OEM guides.
- TOOLS tasks: Optional library of pre-defined connector families with pin maps; validation checks for missing seals/terminals; import/export mappings for PLM/CAD formats.
- COVERAGE tasks: Regression YAMLs covering connectors with cavity tables, shielded cables with drains, splices, protection devices, sealing hardware, and mounting supports.

## Recommendation
ADOPT_LATER — Recommended to formalize these component classes and symbols in Filare after schema/design alignment, so harness outputs match industry expectations without breaking existing users.

## References
- IPC/WHMA-A-620 (Cable and Wire Harness Assemblies)
- ISO 6722-1 / ISO 19642 (Road vehicle cables)
- USCAR-2 (Performance specs for automotive electrical connector systems)
- SAE J1939-13 and SAE J1962 (Diagnostic connectors)
- MIL-STD-5088 (Aircraft wiring practices)
- Typical OEM drafting guides from automotive/aerospace suppliers (TE, Molex, Amphenol, Deutsch)

## Optional Appendix
- Candidate symbol set: rectangular connector blocks with cavity tables; circular connector with backshell; splice barrel/dot symbol; shield drain to ground; fuse/breaker inline symbol; ground lug; P-clamp/edge clip; conduit/heat-shrink notation; label flag at breakout.
- Filare coverage snapshot (schema/docs review):
  - Already covered: connectors with pin tables and labels; connector/cable images and colors; shielded cables (with `s` wire access); bundles; auto-generated single-pin connectors; additional BOM components with qty multipliers (pins, populated, wirecount, terminations, length); basic loop/short notation; per-node styling and hide-disconnected flags.
  - Missing or implicit today (low-friction additions): explicit cavity tables with occupancy/population; terminal/seal/plug part numbers tied to cavities; shield termination metadata (drain, backshell/pigtail target, continuity note); explicit splice/junction type instead of generic connector; protection/support/sealing/label elements as first-class component categories (now only possible via generic additional components); connector family presets (OBD-II, J1939-13, circular/bulkhead) with default pin maps; strain relief/back-shell/boot references and mounting hardware callouts.
