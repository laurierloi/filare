# Mechanical Harness Diagrams and CAD Links

## Summary

Explores how Filare could represent mechanical aspects of harnesses: 2D board/routing diagrams (fixtures, datum, tie-downs) and optional links to CAD/STEP data. Reviews lightweight 2D approaches first, then options to consume CAD/STEP in Python or browser JS for previews or geometry overlays.

## Use Cases for Filare

- Add a 2D mechanical view showing harness routing, clamp positions, grommets, and lengths for board builds.
- Annotate pass-throughs/bulkheads with spatial context and strain-relief details.
- Link to CAD/STEP geometry for reference previews, dimensions, or silhouette extraction without embedding heavy CAD into Filare core.
- Allow browser consumption (HTML output) for interactive previews or measurements.

## Technical Evaluation

- Features (desired): 2D board outline + datum grid; mounting holes/tie-down/clamp positions; pass-throughs and bend radii; harness path polyline with segment lengths; callouts for clips/boots/grommets; optional background from CAD/STEP projection; hyperlinks to external CAD.
- Python options:
  - 2D SVG/canvas: `svgwrite`, `cairosvg`, `matplotlib` (for plotting), `shapely` for geometry ops.
  - DXF export: `ezdxf` for sharing to CAD/laser/board builders.
  - STEP parsing/projection: `pythonocc-core`/`OCP` (OpenCascade bindings), `cadquery` (OCCT wrapper) to load STEP and generate 2D projections; heavier dependency.
  - Meshing/export: `trimesh` + `ocp` pipeline to rasterize silhouettes.
- Browser/JS options:
  - 2D: SVG/Canvas via `Paper.js`, `Two.js`, `Fabric.js` for interactive annotations.
  - 3D/CAD: `three.js` with STEP via `occt-import-js` / `open-cascade.js` for WebAssembly-based STEP parsing; `xeokit` for CAD/IFC/STEP visualization; `3d-tiles`/glTF path if pre-converted.
- Strengths: 2D SVG/DXF is lightweight and aligns with existing Graphviz/HTML flows; CAD links can stay optional; JS viewers enable interactive measure/explode without desktop CAD.
- Weaknesses: OpenCascade bindings add weight/compile time; STEP parsing in-browser via WASM increases bundle size; reliable dimensioning requires units/scale handling.
- Limitations: Full MCAD constraints/clearance checking is out of scope; accurate harness slack/bend modeling would require 3D routing not covered here.
- Compatibility with Filare: 2D overlay can be generated alongside current renders; CAD linkage can be metadata (URL/file ref) or pre-processed silhouettes fed into rendering.
- Required integrations: schema for mechanical view (board outline, features, path points, units), optional CAD references; render pipeline for SVG/DXF export; JS viewer hook in HTML output.

## Complexity Score (1–5)

3 — Adds a parallel 2D mechanical render path and optional CAD linkage. Involves new schema, exporters (SVG/DXF), and optional heavy dependencies (OpenCascade) but does not overhaul core connectivity model.

## Maintenance Risk

- External tools: OpenCascade bindings evolve and can be platform-sensitive; JS STEP viewers rely on WASM builds. SVG/DXF libraries are stable.
- Filare-side: Maintain schema, 2D renderer, and keep optional CAD adapters decoupled to avoid bloating base installs.
- Ongoing cost: Moderate if CAD adapters are optional/plug-in; low for pure 2D SVG/DXF.

## Industry / Business Usage

- Harness board builds use 2D nailboard/fixture drawings with clamp spacing and breakout lengths.
- Automotive/aero teams overlay harness paths on chassis/airframe silhouettes from CAD to check reach and pass-throughs.
- Service/field teams prefer lightweight 2D PDFs/SVG with callouts and lengths; CAD links help for complex areas.

## Who Uses It & Why It Works for Them

- Manufacturing/QA: Needs clamp locations, lengths, and datum for board setup.
- Mechanical/electrical integration teams: Validate routing against chassis/airframe cutouts.
- Service/diagnostics: Quick 2D reference with labels; occasional CAD view for tight packaging zones.

## Feasibility

- Feasible now for 2D SVG/DXF mechanical views with added schema and renderer.
- CAD/STEP linkage feasible if kept optional: parse silhouettes via OpenCascade (Python) or display via JS viewer in HTML.

## Required Work

- REWORK tasks: Define mechanical view schema (units, board outline, datum, path polylines, features like holes/clamps/grommets); ensure outputs directory structure supports mechanical artifacts.
- FEATURE tasks: Implement 2D mechanical renderer (SVG; optional DXF via `ezdxf`); add HTML embed of SVG; add metadata fields for CAD references (file/URL) and optional silhouette background.
- TOOLS tasks: Optional adapters for STEP projection to SVG using `OCP`/`cadquery`; optional JS viewer hook (e.g., three.js + occt-import-js) gated behind a build flag.
- DOCUMENTATION tasks: Syntax examples for mechanical view; guidance on preparing silhouettes from CAD; note optional CAD adapters and size implications.
- COVERAGE tasks: Regression YAMLs with mechanical blocks (board outline, clamps, path, pass-throughs) and optional CAD reference to ensure renders succeed without CAD libs present.

## Recommendation

ADOPT_LATER — Start with pure 2D mechanical view (SVG/DXF) and optional CAD reference fields; add STEP-derived silhouettes/viewers behind optional dependencies after schema stabilizes.

## References

- OpenCascade (OCP/pythonocc-core), cadquery (STEP import/projection)
- ezdxf (DXF creation), svgwrite/cairosvg (SVG)
- three.js + occt-import-js / open-cascade.js for browser STEP viewing
- xeokit SDK (web CAD/IFC/STEP viewer)

## Optional Appendix

- 2D stack: YAML → mechanical schema → SVG/DXF exporter; embed SVG into HTML output.
- CAD flow (optional): STEP → OpenCascade projection → SVG silhouette → overlay in mechanical view; or serve STEP alongside HTML with JS viewer initialized on demand.
