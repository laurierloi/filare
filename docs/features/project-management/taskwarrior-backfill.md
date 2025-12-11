# Taskwarrior Backfill to Backlog

uid: FEAT-PM-0005
status: IN_PROGRESS
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

from: docs/research/project-management.md

## Status

IN_PROGRESS

## Summary

Explore a reverse sync: read Taskwarrior workplans (filtered JSON exports) and backfill updates into the backlog manifest and/or issue headers (status, priority, due) based on UIDs, keeping repo docs in sync with active task lists.

## Requirements

- Consume Taskwarrior JSON exports keyed by the same UIDs used in the backlog manifest.
- Map Taskwarrior fields (status, due, tags) back onto manifest fields without overwriting titles/descriptions.
- Provide a dry-run mode and change report to avoid accidental drift.
- Respect repo authority: manifest remains source of truth; backfill only updates allowed fields (status, due, priority) when newer.
- Support per-file filters (role, milestone) to avoid noisy updates.

## Steps

- [x] Define allowable backfill fields and conflict resolution rules (Taskwarrior vs manifest).
- [x] Implement backfill utility that reads Taskwarrior JSON and proposes manifest/header updates keyed by UID (`scripts/taskwarrior_backfill.py`).
- [x] Add dry-run and report output showing proposed changes before writing (`--apply` to persist).
- [ ] Document workflow and guardrails; clarify that manifest stays authoritative.

## Progress Log

- 2025-02-19: Drafted feature; awaiting approval.

## Sub-Features

- None.

## Related Issues

- docs/issues/backlog-header-normalization.md
- docs/features/project-management/taskwarrior-pipeline.md
