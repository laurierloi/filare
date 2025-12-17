# Taskwarrior Workflow — Agent Roles

Use Taskwarrior to pull the next ready task assigned to your agent type, ensuring dependencies are respected.

## Steps

1. Sync backlog from Taskwarrior export/backfill (ensure latest JSON is applied).
2. List ready tasks for your role (no blocked dependencies):
   - Preferred: `just taskwarrior-next role=<ROLE> limit=5`
   - Taskwarrior native: `task +role:<ROLE> status:pending -BLOCKED next`
3. Start the top task:
   - `task <id> start`
4. When done, close it:
   - `task <id> done` (or `just taskwarrior-update uid=<UID> done=true note="..."` to stamp completion and add a note).
5. If blocked/missing info, annotate and set `wait:` or `scheduled:` to pause it, then pick the next ready item.

## Notes

- Roles align to AGENT guides (e.g., FEATURE, TOOLS, DOCUMENTATION, UI, VALIDATOR).
- Do not start tasks with unresolved dependencies; rely on the ready filter above.
- Keep annotations brief and action-focused for handoff back to Project Manager.
