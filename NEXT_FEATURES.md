# Next Features: Configuration Models, Graphs, and Template Inputs

## Overview
We need to separate configuration (YAML-derived) data, rendering/template inputs, and semantic graph links. This document captures concrete, small tasks to reach that goal incrementally.

## Tasks (each should be a small, self-contained step)
1) Add Pydantic BaseModels for configuration (YAML-facing) entities:
   - ConnectorConfig (designator, pins, pinlabels, pincolors, style, loops, images, notes, etc.)
   - CableConfig (designator, wirecount, colors, wirelabels, shields, bundles, length/gauge)
   - WireConfig (color, label, gauge, length)
   - ConnectionConfig (from/to references, via cable/wire identifiers)
   - MetadataConfig (title, pn, company, authors, revisions, template, etc.)
   - PinConfig (id/label/color per pin)
   - PageOptionsConfig (diagram/page options) aligned to YAML

2) Add round-trip tests for each config model:
   - Load minimal YAML snippets into config models, validate, dump back to dict/YAML, and compare expected fields.
   - Cover known example/tutorial snippets to ensure compatibility.

3) Adapt existing dataclasses incrementally to accept config models:
   - Step A: Component/Connector/Cable constructors accept corresponding Config models and map fields.
   - Step B: Ensure BOM population and rendering still work using config-backed construction.
   - Add unit tests per class to verify construction from Config models yields identical behavior as before.

4) Define template-input models:
   - Create explicit models for what templates need (e.g., TemplateConnector, TemplateCable, TemplateBOMItem).
   - Add conversion helpers from config models (or existing dataclasses) to template models.
   - Add tests that convert known fixtures to template models and assert required fields are present.

5) Plan/implement semantic graph models:
   - Graph nodes/edges for: Pins → Interfaces (e.g., RS422/Ethernet/CAN), Bundles ↔ Cables/Wires, Cable segments.
   - Implement a simple graph representation layer (nodes/edges) to link configuration entities.
   - Add tests that build small graphs from config models (e.g., one connector with an RS422 interface and a bundled cable) and verify adjacency/labels.

6) Map graphs to template representations:
   - Add mappers that transform graph nodes/edges into template-input models.
   - Add tests ensuring a graph built from config models renders expected template inputs (IDs, labels, per-harness info).

7) Incremental migration steps (one per commit):
   - Step 1: Introduce ConnectorConfig with tests.
   - Step 2: Introduce CableConfig/WireConfig with tests.
   - Step 3: Introduce ConnectionConfig with tests.
   - Step 4: Introduce MetadataConfig/PageOptionsConfig with tests.
   - Step 5: Wire dataclasses to accept ConnectorConfig in constructors; add regression tests.
   - Step 6: Wire Cable dataclass to accept CableConfig; add regression tests.
   - Step 7: Add template-input models and conversions; add tests.
   - Step 8: Add initial graph structures and mappings; add tests.

8) Documentation updates:
   - Document config models, template-input models, and graph mappings.
   - Add examples of round-trip YAML → Config → Template → Render flow.

9) Performance/compatibility safeguards:
   - Keep legacy dataclasses intact until config and template models fully cover existing behavior.
   - Add regression tests comparing BOM/HTML/TSV outputs before/after migrations.

