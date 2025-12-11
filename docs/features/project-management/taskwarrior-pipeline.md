# Taskwarrior Backlog Export

uid: FEAT-PM-0006
status: BACKLOG
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

Build a Taskwarrior export pipeline that converts the backlog manifest (uids + metadata) into an importable JSON task list with tags, dependencies, and due dates aligned to Filare milestones.

## Requirements

- Consume the canonical backlog manifest keyed by `uid` and source file path.
- Emit Taskwarrior-compatible JSON or task lines with:
  - `description` referencing the `uid` and title.
  - `project` set to `filare` (or configurable).
  - `tags` derived from owner_role, milestone, and workstream/module.
  - `depends` populated with upstream UIDs.
  - Optional `due` from milestone target or explicit date.
- Support filtered exports by role/project/priority/milestone so lists stay short (e.g., `docs/task/workplan/taskwarrior-cli-high.json`, `docs/task/workplan/taskwarrior-tools-q1.json`).
- Output location pattern: `docs/task/workplan/taskwarrior-<description>-<filters>.json` (plus optionally `outputs/workplan/` for generated artifacts).
- Regeneration via `just workplan` (or similar) alongside other planning artifacts.
- Non-destructive updates: allow merging/updating tasks when UIDs already exist instead of always overwriting the full list.
- Enforce UID format (`ISS-####`, `FEAT-<AREA>-####`) as the stable identifier across all exports.

## Steps

- [x] Define the manifest fields required for Taskwarrior (title, uid, role, milestone, dependencies, due/estimate).
- [x] Implement exporter that reads backlog headers and writes exports to `outputs/workplan/taskwarrior.json` (filterable via CLI).
- [x] Add filter support (role, priority, milestone, status) via CLI arguments to keep exports scoped.
- [x] Provide regeneration command: `just taskwarrior-export` (calls `scripts/export_taskwarrior.py`).
- [ ] Support non-destructive merges when regenerating existing files (current behavior overwrites).
- [ ] Validate output against Taskwarrior import (schema/format) and add a minimal test fixture.
- [ ] Document usage: how to regenerate and import into Taskwarrior, plus examples of filtered exports.

## Progress Log

- 2025-02-19: Drafted feature; awaiting approval.

## Sub-Features

- None.

## Related Issues

- docs/issues/backlog-header-normalization.md
- docs/features/project-management/project-management-planning.md
