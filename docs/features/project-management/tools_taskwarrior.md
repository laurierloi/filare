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
- Taskwarrior helper/queries that list the next task for a given agent role, excluding blocked items.
- Pool splitter that enforces dependency isolation and exports per-pool views.
- Documentation updates:
  - Visualization of pools.
  - `docs/workflows/taskwarrior-agent.md`
  - `docs/workflows/taskwarrior-project-manager.md`

## Open Questions
- Pool sizing policy: fixed N per operator input, or dynamic based on active agents?
- Where to store per-pool exports (e.g., `outputs/taskwarrior/pool-*.json`)?
- Priority rules when pools have uneven loads.
