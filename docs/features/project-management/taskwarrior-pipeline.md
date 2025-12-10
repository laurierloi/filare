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

BACKLOG

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

- [ ] Define the manifest fields required for Taskwarrior (title, uid, role, milestone, dependencies, due/estimate).
- [ ] Implement exporter that reads the manifest and writes filtered exports to `docs/task/workplan/taskwarrior-<description>-<filters>.json` (and optional aggregate output).
- [ ] Add filter support (role, project/workstream, priority, milestone) via config or CLI arguments to keep exports scoped.
- [ ] Support non-destructive updates: merge on UID (update fields rather than overwrite) when regenerating existing files.
- [ ] Validate output against Taskwarrior import (schema/format) and add a minimal test fixture.
- [ ] Document usage: how to regenerate and import into Taskwarrior, plus examples of filtered exports.

## Progress Log

- 2025-02-19: Drafted feature; awaiting approval.

## Sub-Features

- None.

## Related Issues

- docs/issues/backlog-header-normalization.md
- docs/features/project-management/project-management-planning.md
