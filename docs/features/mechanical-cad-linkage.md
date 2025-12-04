from: docs/research/mechanical-harness-diagrams.md

# Mechanical CAD/STEP Linkage and Viewer

## Status
PROPOSED

## Priority
Low

## Summary
Provide optional CAD/STEP linkage for mechanical harness context: reference a CAD file/URL, optionally generate 2D silhouettes from STEP via OpenCascade, or embed a browser viewer (three.js + occt-import-js/open-cascade.js or xeokit) in HTML output for inspection.

## Motivation
- Integration teams sometimes need CAD context for pass-throughs and packaging; a lightweight viewer beats forcing desktop CAD for every stakeholder.

## Affected Users / Fields
- Mechanical/electrical integration teams
- Packaging/EMI reviewers
- Advanced manufacturing teams needing CAD reference alongside 2D boards

## Scope
- Optional metadata in mechanical block to point to CAD/STEP files/URLs.
- Optional server-side silhouette generation from STEP to SVG for overlay.
- Optional client-side viewer hook in HTML to load STEP when available.

## Out of Scope
- Full 3D routing or clearance checks.
- Mandatory CAD dependencies in the default install.

## Requirements
- CAD reference fields are optional and ignored when absent.
- Silhouette generation (if enabled) uses optional OCCT bindings (OCP/cadquery); guarded so base users are unaffected.
- HTML output can initialize a JS viewer when provided with a STEP/glTF URL; include a minimal loader stub and document how to bundle viewer assets.

## Steps
- [ ] Add optional CAD reference fields to mechanical schema (file/URL, unit hints).
- [ ] Define optional silhouette generation path using OCCT (behind feature flag/dependency check) to produce SVG overlays.
- [ ] Add HTML hook for client-side viewer (three.js + occt-import-js/open-cascade.js or xeokit), disabled by default unless assets/URL provided.
- [ ] Document setup: how to supply STEP, enable silhouette generation, or host viewer assets; include example YAML.
- [ ] Add regression YAML ensuring base rendering ignores CAD fields when not enabled.

## Progress Log
- PROPOSED — created from mechanical harness research.

## Validation
- Regression YAML with CAD reference fields confirming base renders still succeed without CAD libs.
- Optional: sample with provided STEP + silhouette generation (manual check if OCCT installed).

## Dependencies / Risks
- OpenCascade/JS viewer assets can bloat footprint; must remain optional.
- Browser-side STEP parsing relies on WASM bundles; need clear guidance for hosting assets.
