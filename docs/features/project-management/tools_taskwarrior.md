# Taskwarrior Backlog Tools

## Goals
- Provide a Taskwarrior workflow so each agent can pull the next ready task from a shared pool.
- Allow splitting the backlog into N independent pools (one per agent) with no cross-pool dependencies.
- Improve documentation to visualize task pools and clarify usage.

## Proposed Work
- Implement a Taskwarrior helper that surfaces the next unblocked task per agent role (uses existing export/backfill flow).
- Add pool-sharding logic: partition tasks into N pools with dependency checks; refuse to assign dependents across pools.
- Add docs:
  - Visual overview of pools and readiness (Mermaid/Graphviz).
  - Per-role workflows for Taskwarrior usage.

## Deliverables
- Taskwarrior helper/queries that list the next task for a given agent role, excluding blocked items. (**done** via `just taskwarrior-next`)
- Pool splitter that enforces dependency isolation and exports per-pool views. (**done** via `just taskwarrior-pools`)
- Documentation updates:
  - Visualization of pools (describe pool JSON + Mermaid/Gantt usage). (**done**)
  - `docs/workflows/taskwarrior-agent.md` (**done**)
  - `docs/workflows/taskwarrior-project-manager.md` (**done**)
- Status/note updater with completion stamp. (**done** via `just taskwarrior-update`)

## Open Questions
- Pool sizing policy: fixed N per operator input, or dynamic based on active agents?
- Where to store per-pool exports (e.g., `outputs/taskwarrior/pool-*.json`)? **Current**: `outputs/workplan/taskwarrior-pool-<n>.json`.
- Priority rules when pools have uneven loads.

## Usage (current)
- Export backlog: `just taskwarrior-export` (writes `outputs/workplan/taskwarrior.json`).
- Next ready tasks per role: `just taskwarrior-next role=FEATURE limit=5`.
- Split into dependency-safe pools: `just taskwarrior-pools pools=3` (writes `outputs/workplan/taskwarrior-pool-*.json`; no cross-pool deps).
- Visualize pools: load `taskwarrior-pool-*.json` into your preferred viewer or combine with Mermaid/Gantt (`just mermaid-gantt`) to confirm pool coverage.
- Update status/notes with optional completion stamp: `just taskwarrior-update uid=<UID> status=IN_PROGRESS note="..." done=true`.
