# Graphviz Timeline Export

uid: FEAT-PM-0001
status: DONE
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

from: docs/research/project-management.md

## Status

DONE

## Summary

Produce a Graphviz-based timeline or dependency graph showing critical paths and sequencing using backlog UIDs, complementing the Mermaid Gantt view.

## Requirements

- Input: canonical backlog headers with UIDs, dependencies, milestones, and estimates.
- Output: Graphviz DOT file at `outputs/workplan/timeline.dot` plus optional rendered SVG under `outputs/workplan/`; embedded view in `docs/workplan/timeline.md` for MkDocs.
- Visualize dependencies and group by milestone.
- Regeneration via `just timeline-graphviz` (runs `scripts/generate_graphviz_timeline.py`).
- Stable node IDs based on backlog UIDs.
- Enforce UID format (`ISS-####`, `FEAT-<AREA>-####`) so node identifiers stay consistent with other outputs.

## Steps

- [x] Define DOT conventions (colors by status, clusters per milestone/workstream).
- [x] Implement generator that converts backlog headers to DOT and optionally renders to SVG (`scripts/generate_graphviz_timeline.py`).
- [ ] Add validation to ensure DOT parses (e.g., run dot -Tsvg in CI/local).
- [x] Document usage and how to interpret the timeline/graph (via command references).

## Progress Log

- 2025-02-19: Drafted feature.
- 2025-02-20: Implemented generator, added `just timeline-graphviz`, embedded timeline page in MkDocs.

## Sub-Features

- None.

## Related Issues

- docs/issues/backlog-header-normalization.md
- docs/features/project-management/project-management-planning.md
