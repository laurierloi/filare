# Taskwarrior Workflow — Project Manager

Use Taskwarrior to publish ready queues per agent, enforce dependency order, and shard the backlog when multiple agents work in parallel.

## Steps
1. **Ingest sources:** Refresh tasks from `docs/features/**`, `docs/issues/**`, `docs/workplan/**`; update priorities/dependencies.
2. **Export/Backfill:**
   - Export current Taskwarrior state: `just taskwarrior-export`
   - Backfill from JSON (dry-run): `just taskwarrior-backfill`
   - Apply backfill: `just taskwarrior-backfill-apply`
3. **Shard pools (when N agents run in parallel):**
   - Partition tasks into N pools by role/priority: `just taskwarrior-pools pools=<N>` (writes `outputs/workplan/taskwarrior-pool-*.json`).
   - Ensure no cross-pool dependency; reassign or reorder until pools are independent.
4. **Publish ready queues:**
   - For each pool/role: provide the ready filter (`task +role:<ROLE> status:pending -BLOCKED next`) or `just taskwarrior-next role=<ROLE>`.
   - Export per-pool JSON for clarity (see pool outputs).
5. **Monitor & adjust:**
   - Rebalance pools if one agent drains early.
   - Update priorities/dates based on operator feedback and dependency changes.

## Notes
- Keep pools dependency-free; if impossible, merge affected tasks into the same pool.
- Annotate tasks with source doc path and target date to maintain traceability.
- Provide agents a short “next up” list per role after each planning cycle.
