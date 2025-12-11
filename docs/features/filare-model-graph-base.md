# FilareModel Graph Base

uid: FEAT-GRAPH-0001
status: IN_PROGRESS
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Status

IN_PROGRESS

## Summary

Introduce a shared FilareModel base for all models under `src/filare/models`, ensuring each instance carries a UUID4 identifier and participates in a graph of node/link relationships.

## Requirements

- Add a FilareModel base with a required unique `id` generated as a random UUID4; IDs remain internal (not user-supplied) but must persist across in-memory structures and intermediate serialization.
- Keep objects free of link bookkeeping; objects only carry their UUID. A separate graph structure manages connectivity so objects do not need updates when links change.
- Maintain a separate UUID→object map to resolve node/link IDs to concrete model instances.
- Represent links via a dedicated `FilareLink` base model (and subclasses) with `(link_uuid, src_uuid, target_uuid)`; link instances live in the UUID→object map.
- Provide an exportable `graph` block (for debug/export) holding only IDs, with minimal shape: `graph: { nodes: [{id}], links: [{id, src, tgt, type?, data?}] }`. Default is internal-only; not required in user-authored YAML.
- Migrate existing models in `src/filare/models` to derive from or embed FilareModel so they participate in the graph.
- Keep YAML schema and rendered outputs backward compatible; any new identifiers or links must be optional/derived so existing inputs remain valid.
- Document how nodes/links are generated and consumed, and add tests/examples that exercise the graph behavior once implemented.

## Open Questions

- None (serialization is internal; `graph` export is optional and minimal).

## Graph Examples (debug/export)

Minimal export view (IDs only; objects resolved via UUID→object map):

```yaml
graph:
  nodes:
    - id: "c2f7...d2"
    - id: "7b8a...41"
  links:
    - id: "e91a...9c"
      src: "c2f7...d2"
      tgt: "7b8a...41"
      type: connection # FilareLink subclass discriminator (optional)
      data: {} # optional link parameters
```

Notes:

- The graph block is generated for internal/export/debug flows; users do not author it.
- Objects keep only their UUID; the graph owns connectivity.
- UUID→object map remains internal and is the lookup for both nodes and links.

## Steps

- [ ] Finalize FilareModel/graph design: internal UUID4s on models, linkless objects, UUID→object map, FilareLink base, exportable minimal `graph` block.
- [ ] Implement FilareModel base and FilareLink base; add UUID assignment and link registry plumbing.
- [ ] Migrate models in `src/filare/models` to use FilareModel (inherit/compose) without breaking existing schemas.
- [ ] Add internal graph builder/registry and optional `graph` export path; ensure links serialize as UUID strings and deserialize to UUID objects.
- [ ] Add docs/tests/examples demonstrating graph export/debug and validate CLI renders/BOM remain compatible.
- [ ] Finalize feature documentation and mark the feature complete.

## Progress Log

2025-12-06: Created initial feature spec draft for FilareModel graph base and awaiting operator review.
2025-12-06: Updated link design per operator: FilareModel holds link UUIDs; link objects live in a UUID→object map.
2025-12-06: Clarified that IDs are internal-only (UUID4), links serialize as UUID strings, deserialize as UUIDs, and links extend a `FilareLink` base.
2025-12-06: Added graph export shape (nodes/links with IDs only), affirmed linkless objects with UUIDs, and outlined implementation steps.
2025-12-06: Added follow-up subfeatures under `docs/features/graph/` for pins, wires, colors, connections, attachments, BOM traversal, bundles/cables-as-part, and part linkage.

## Sub-Features

- graph/pins-in-graph.md
- graph/wires-in-graph.md
- graph/colors-in-graph.md
- graph/connections-in-graph.md
- graph/connector-cable-connector-in-graph.md
- graph/bom-from-graph.md
- graph/cut-diagram-from-graph.md
- graph/termination-diagram-from-graph.md
- graph/bundle-model.md
- graph/cable-as-part.md
- graph/parts-and-components-links.md
- graph/parts-list-export.md
- graph/interface/interface-general-idea.md
- graph/pins-terminations-in-graph.md
- graph/pin-ordering-parser.md
- graph/render-metadata-separation.md

## Related Issues

- None
