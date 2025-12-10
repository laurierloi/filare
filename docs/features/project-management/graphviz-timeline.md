# Graphviz Timeline Export

uid: FEAT-PM-0001
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

Produce a Graphviz-based timeline or dependency graph showing critical paths and sequencing using backlog UIDs, complementing the Mermaid Gantt view.

## Requirements

- Input: canonical backlog manifest with UIDs, dependencies, milestones, and estimates.
- Output: Graphviz DOT file at `outputs/workplan/timeline.dot` plus optional rendered SVG/PNG under `outputs/workplan/`.
- Visualize dependencies and highlight critical items (high priority/high risk) and milestone groups.
- Regeneration via `just workplan` (or similar) in the same pipeline as Taskwarrior and Mermaid outputs.
- Stable node IDs based on backlog UIDs.
- Enforce UID format (`ISS-####`, `FEAT-<AREA>-####`) so node identifiers stay consistent with other outputs.

## Steps

- [ ] Define DOT conventions (colors for priority/risk, clusters per milestone/workstream).
- [ ] Implement generator that converts manifest to DOT and optionally renders to SVG/PNG.
- [ ] Add validation to ensure DOT parses (e.g., run dot -Tsvg in CI/local).
- [ ] Document usage and how to interpret the timeline/graph.

## Progress Log

- 2025-02-19: Drafted feature; awaiting approval.

## Sub-Features

- None.

## Related Issues

- docs/issues/backlog-header-normalization.md
- docs/features/project-management/project-management-planning.md
