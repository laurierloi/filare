# Backlog Planning Pipeline

uid: FEAT-PM-0004
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

from: docs/research/project-management.md

## Status

BACKLOG

## Summary

Define a planning pipeline that turns `docs/issues` and `docs/features` into synchronized work artifacts: a Taskwarrior task list, Mermaid Gantt charts, and optional Graphviz timelines, all keyed by immutable UIDs to keep references stable for agents and users.

## Requirements

- Every issue/feature carries a structured header with an immutable `uid`, status, priority, owner/role, estimate, dependencies, risk, and milestone.
- UID format is standardized: issues use `ISS-<4 digits>`; features use `FEAT-<AREA>-<4 digits>` (e.g., FEAT-CLI-0003), with AREA codes such as CLI/RENDER/GRAPH/BOM/MECH/DOCS/TOOLS/PERF/UI.
- A single backlog manifest maps these UIDs to their source files and aggregates metadata for generation.
- Outputs are generated separately and kept in sync:
  - Taskwarrior JSON import for CLI task tracking (tags = role/milestone/module).
  - Mermaid Gantt charts grouped by milestone/workstream for docs.
  - Optional Graphviz timeline for alternative visualization.
- Provide a workflow doc explaining how to add/update items, refresh artifacts, and avoid conflicts.
- Keep changes non-invasive to Filare core (docs + tooling only) and friendly to offline execution.

## Steps

- [ ] Design the backlog manifest format (YAML/JSON) keyed by `uid`, covering roles, dependencies, milestones, and source file paths.
- [ ] Define output locations and regeneration commands (e.g., `just workplan`) for Taskwarrior JSON, Mermaid Gantt, and Graphviz timeline.
- [ ] Implement the generator that reads the manifest and emits the three outputs with consistent IDs and links back to the markdown sources.
- [ ] Add documentation for contributors/agents on claiming work, refreshing outputs, and conflict avoidance.
- [ ] Pilot the pipeline on a subset of issues/features and validate round-trip (manifest ↔ outputs) before scaling to all items.

## Progress Log

- 2025-02-19: Feature drafted from project-management research; awaiting approval.

## Sub-Features

- taskwarrior-pipeline
- mermaid-gantt
- graphviz-timeline
- taskwarrior-backfill

## Related Issues

- docs/issues/backlog-header-normalization.md
