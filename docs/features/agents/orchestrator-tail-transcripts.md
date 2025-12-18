# Tail and transcript streaming for orchestrated sessions

uid: FEAT-TOOLS-0013
status: BACKLOG
priority: medium
owner_role: TOOLS
estimate: TBD
dependencies: [FEAT-TOOLS-0006]
risk: medium
milestone: backlog

## Summary

Provide per-session tailing and structured transcript streaming (NDJSON with metadata) so operators can monitor agent output without cross-talk and capture logs for review.

## Proposal

- Extend IO layer to support streaming tmux pane output to host files (`outputs/agents/<role>/<session>/transcript.ndjson`) with fields: timestamp, direction, session_id, branch, text.
- CLI: `orchestrator tail --session-id ... [--follow]` and just wrapper `orchestrator-tail`.
- Optional: snapshot vs. follow modes; rate-limit to avoid log bloat.

## Verification & Validation

- Tail shows only the target session and follows live output.
- NDJSON transcript files are written with correct metadata and are readable after session ends.

## Dependencies

- IO routing from `FEAT-TOOLS-0006`; labels/discovery from `FEAT-TOOLS-0012`.
