# Prompt integration with lifecycle/IO

uid: FEAT-TOOLS-0014
status: BACKLOG
priority: medium
owner_role: TOOLS
estimate: TBD
dependencies: [FEAT-TOOLS-0005, FEAT-TOOLS-0006, FEAT-TOOLS-0007]
risk: medium
milestone: backlog

## Summary

Wire operator prompts into lifecycle and IO flows so approval boundaries (network, destructive commands, etc.) automatically enqueue prompts and inject operator decisions back into the agent session.

## Proposal

- Define trigger points (execute vs dry-run, network access, destructive commands) that emit `requires_operator` messages via IO layer.
- Orchestrator consumes these messages, adds to the feedback queue, and pauses the session (detach IO).
- On approval/reject via feedback CLI, orchestrator sends the decision into the session (via `send`) and resumes.
- Respect per-session policy from manifest (`requires_approval_for`, `auto_allow` lists).

## Verification & Validation

- Simulated prompt triggers are enqueued with correct metadata; session pauses.
- Approve/reject paths send replies and resume/stop as expected.
- Prompts persist across orchestrator restarts; dashboard reflects pending counts.

## Dependencies

- Lifecycle (`FEAT-TOOLS-0005`), IO (`FEAT-TOOLS-0006`), feedback queue (`FEAT-TOOLS-0007`), labels (`FEAT-TOOLS-0012`).
