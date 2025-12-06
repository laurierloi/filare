# Renderer Plugin Registry

## Summary

Suggest introducing a renderer/plugin registry to decouple output formats from CLI logic. Instead of hardcoding format codes and branching per type, a registry would map format keys to renderer classes/functions with declared capabilities and dependencies, simplifying extension (e.g., cut/termination diagrams, new exports).

## Use Cases for Filare

- Adding new outputs (e.g., DXF/CAD, JSON summaries) without editing CLI conditionals.
- Allowing downstream harnesses to register custom renderers.
- Enabling selective runs (subset of outputs) driven by config/labels in CI.
- Centralizing renderer metadata (needs Graphviz, produces HTML/PNG, supports PDF bundling).

## Technical Evaluation

- Features: A registry keyed by format (string/enum) storing renderer callables and metadata (input type, produces files, side effects). CLI and flows resolve requested formats through the registry and execute in dependency order (e.g., HTML before PDF bundle).
- Strengths: Reduces branching in `cli.py` and flow modules; supports external/plugin renderers; makes capabilities discoverable; improves testability of render selection.
- Weaknesses: Requires refactoring current format handling and PDF bundling logic; needs dependency ordering to avoid missing prerequisites.
- Limitations: Some renderers (PDF bundle) are composite and need awareness of other outputs.
- Compatibility with Filare: Works with current render functions (`render/html.py`, `render/graphviz.py`, `render/output.py`); registry can wrap these without changing rendering internals initially.
- Required integrations: Define registry module; refactor CLI format parsing to use it; add metadata for each renderer (inputs, outputs, dependencies).

## Complexity Score (1–5)

**4** — Touches CLI, flows, and render modules; requires careful ordering and backward compatibility for format codes/flags.

## Maintenance Risk

- Filare-side: Medium during migration; long-term improvement by isolating renderer definitions.
- External: None; registry is internal; dependencies remain (Graphviz, etc.).
- Ongoing cost: Low; adding new renderers becomes a registry entry + docs/tests.

## Industry / Business Usage

- Build systems and SSGs (webpack loaders, Sphinx builders) use registries/plugins to add outputs without core edits.
- Python imaging/reporting tools (Pillow plugins, Pandas to\_\* exporters) rely on registries to manage formats and capabilities.

## Who Uses It & Why It Works for Them

- **Sphinx builders**: New builders register once; CLI stays stable while outputs expand.
- **Webpack/Rollup**: Plugin registries manage transforms and outputs cleanly.
- **Pandas**: to\_\* exporters are discoverable and independently testable.

## Feasibility

- Feasible with a staged migration: introduce registry alongside existing logic, then switch CLI/flows once parity is validated.

## Required Work

- **REWORK tasks**: Create renderer registry abstraction (format key, callable, metadata, dependencies); register existing renderers (HTML/SVG/PNG/TSV shared BOM, PDF bundler); update CLI/flows to resolve requested formats through registry; maintain mapping from current short codes to registry keys.
- **FEATURE tasks**: Allow third-party/experimental renderers to self-register; expose `filare --list-formats` using registry metadata.
- **DOCUMENTATION tasks**: Developer guide for adding renderers; user doc for available formats and dependencies.
- **TOOLS tasks**: Optional sanity check tool to validate registry entries and dependencies.
- **COVERAGE tasks**: Tests for registry resolution, dependency ordering, and backward-compatible format parsing.

## Recommendation

**ADOPT_LATER** — Valuable for extensibility but should follow configuration/pipeline cleanup to reduce migration risk.

## References

- Plugin/registry patterns from Sphinx builders, webpack loaders, and Pandas exporters.

## Optional Appendix

- Example registry entry:
  - key: `html`
  - callable: `render.html.generate_html`
  - deps: `graphviz` (SVG), produces `*.html`, supports PDF bundling flag.
