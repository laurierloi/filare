from: docs/features/graph/connections-in-graph.md

uid: FEAT-GRAPH-0015
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Render Metadata Separation

## Status

PLANNED

## Summary

Explore decoupling rendering metadata (side/label/visual hints) from graph link payloads by introducing dedicated nodes or structures, so graph semantics remain pure while rendering concerns are layered separately.

## Requirements

- Identify rendering metadata currently carried on links (e.g., side, label, visual hints) that could be separated from semantic link data.
- Propose a structure (e.g., RenderMetadata nodes keyed by link UUID) to hold rendering hints without altering graph semantics.
- Ensure backward compatibility: default behavior matches current rendering; separation is optional/transparent to users.
- Document migration path and how renderers should resolve metadata vs. semantic links.

## Steps

- [ ] Catalog rendering metadata on existing/planned link payloads (connections, attachments, etc.).
- [ ] Design a decoupled representation (nodes or auxiliary mapping) and resolution rules.
- [ ] Add tests/examples to validate rendering parity with/without separated metadata.
- [ ] Document the approach and update progress.
- [ ] Finalize and mark feature complete.

## Progress Log

2025-12-06: Created follow-up feature spec to separate rendering metadata from link payloads.

## Sub-Features

- None

## Related Issues

- docs/features/graph/connections-in-graph.md
