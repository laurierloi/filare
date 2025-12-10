# Mermaid Gantt Backlog Charts

from: docs/research/project-management.md

## Status

BACKLOG

## Summary

Generate Mermaid Gantt charts from the backlog manifest to visualize milestones, dependencies, and sequencing for Filare workstreams.

## Requirements

- Use the canonical manifest keyed by `uid` to build Gantt sections per workstream/milestone.
- Include dependency ordering (`after <id>`) based on manifest dependencies.
- Output location: `outputs/workplan/gantt.md` (Mermaid blocks embeddable in docs).
- Regeneration via `just workplan` (or similar) with other planning artifacts.
- Keep identifiers stable (uids) for cross-linking to issues/features.
- Enforce UID format (`ISS-####`, `FEAT-<AREA>-####`) for consistent references in diagrams.

## Steps

- [ ] Define mapping from manifest fields to Gantt (sections, start dates, durations/estimates, dependencies).
- [ ] Implement generator producing Mermaid blocks grouped by milestone/workstream.
- [ ] Add validation or linting step to ensure Mermaid syntax correctness.
- [ ] Document embedding instructions for docs/mkdocs and regeneration workflow.

## Progress Log

- 2025-02-19: Drafted feature; awaiting approval.

## Sub-Features

- None.

## Related Issues

- docs/issues/backlog-header-normalization.md
- docs/features/project-management/project-management-planning.md
