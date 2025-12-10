# Config and graph modeling

uid: FEAT-CONFIG-GRAPH-0001
status: PLANNED
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: beta

## Summary

Introduce structured config models and a small graph representation to drive template inputs, enabling round-trip YAML config, tool-specific graph config (pydeps/grimp/pyan3), and future networkx-based analyses.

## Requirements

- Add YAML-facing Config models (ConnectorConfig, CableConfig, WireConfig, ConnectionConfig, MetadataConfig, PageOptionsConfig, PinConfig) with round-trip tests.
- Add template-input models (TemplateConnector/TemplateCable/TemplateBOMItem, etc.) and mapping from configs/BaseModels to template inputs.
- Build a minimal graph representation (nodes/edges for pins/interfaces/bundles/segments) to support template input generation and future analyses.
- Wire flows to accept the config models, convert to BaseModels/graph, and keep legacy behavior stable.
- Add CLI/tooling support for code-graph configs (pydeps/grimp/pyan3) and document the config schema.

## Steps

- [ ] Define config schemas and validators; add round-trip YAML tests.
- [ ] Implement graph builder and mapping to template-input models.
- [ ] Integrate into build/render flows with backward-compatible switches.
- [ ] Document the config schema and graph flow; add regression examples.

## Related Items

- RefactorPlan step 4 and 7 (config and template inputs).
- `docs/tasks.md`: networkx/config graph tasks.
- `docs/features/config/code_graph.md` (code graph tooling configs).
