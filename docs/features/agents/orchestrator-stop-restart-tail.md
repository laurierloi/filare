# Orchestrator stop/restart/tail commands

uid: FEAT-TOOLS-0011
status: BACKLOG
priority: medium
owner_role: TOOLS
estimate: TBD
dependencies: [FEAT-TOOLS-0005, FEAT-TOOLS-0006]
risk: medium
milestone: backlog

## Summary

Add CLI/just wrappers to stop, restart, and tail logs for specific orchestrated sessions using registry/labels for discovery, so operators can manage containers without manual docker commands.

## Proposal

- Extend `orchestrator.cli` with `stop --session-id ...`, `restart --session-id ...`, and `tail --session-id ... [--follow]`.
- Use container labels (`filare.session`, `filare.role`, `filare.branch`) to find the container; fallback to registry state if labels missing.
- `tail` should stream tmux pane or docker logs per session (no cross-talk).
- Add just wrappers: `orchestrator-stop`, `orchestrator-restart`, `orchestrator-tail`.

## Verification & Validation

- Stopping a session terminates the correct container; registry updated to `stopped`.
- Restart relaunches using the same manifest/workspace and records new state.
- Tail shows only the target session’s output; follows until interrupted.

## Dependencies

- Lifecycle/state in `FEAT-TOOLS-0005`; IO routing in `FEAT-TOOLS-0006`.

## Progress / Notes

- Added label-based `stop`, `restart`, and `tail` commands in `orchestrator.cli` plus just wrappers. Restart reuses manifest to relaunch; stop/tail locate containers via labels.
- Next: update registry state on stop/restart and consider tmux-pane-specific tail with NDJSON transcripts (see `FEAT-TOOLS-0013`).
