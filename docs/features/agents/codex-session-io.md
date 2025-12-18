# IO routing for orchestrated codex sessions

uid: FEAT-TOOLS-0006
status: BACKLOG
priority: medium
owner_role: TOOLS
estimate: TBD
dependencies: [FEAT-TOOLS-0002, FEAT-TOOLS-0005]
risk: medium
milestone: backlog

## Summary

Design the read/write channels that let the ORCHESTRATOR agent send instructions to a specific codex session and capture its responses/logs without cross-talk. Provide structured transcripts stored under `outputs/agents/<role>/<session-id>/`.

## Motivation

- Multi-agent runs need deterministic routing of prompts and outputs.
- Operator auditing requires durable transcripts and metadata.
- Future automation (summaries, dashboards) depends on structured logs.

## Proposal

- Inside each container, run codex under a `tmux` session named after `session_id`.
- For writes: orchestrator uses `docker exec -i <cid> tmux send-keys -t <session> "<payload>" Enter` to deliver commands/messages (or via a lightweight stdin pipe created at launch).
- For reads: tail a named pipe or tmux pipe to a log file mounted to host (e.g., `/home/agent/workspace/.orchestrator/<session>.log` bound to `outputs/agents/.../log.txt`), and optionally stream via `docker logs -f` if stdout is forwarded.
- Normalize message envelopes with metadata (`timestamp`, `direction`, `from`, `session_id`, `branch`, `requires_operator`, `tags`) in NDJSON stored alongside raw text.
- Provide helper functions: `send_message(session_id, text)`, `stream_logs(session_id, follow=True)`, `snapshot_transcript(session_id)`.
- Guardrails: rate-limit sends, chunk large messages, and clearly mark system-inserted notes (e.g., operator replies).
- Reconnect support: when the orchestrator process restarts, offer a `resume-all` flow that reattaches to existing tmux sessions/containers by reading the registry and reestablishing log streams without restarting containers.

## Verification & Validation

- Send commands to two running sessions and confirm logs show only targeted messages.
- Log files should accumulate NDJSON entries with accurate timestamps and directions.
- Killing a session should stop streaming without blocking other sessions; reattach after restart.
- Optional: run a dry-run mode that mocks docker exec to test parsing without containers.
- Optional: add agent-marked pytest coverage under `agents/tests/` to validate NDJSON envelope structure (including branch), per-session isolation, and send/receive mocks without touching real docker/tmux.

## Dependencies

- Requires lifecycle and registry from `FEAT-TOOLS-0005`.
- Consumed by operator feedback loop (`FEAT-TOOLS-0007`) and CLI tools (`FEAT-TOOLS-0008`).

## Progress / Notes

- Added `resume-all` support in CLI/runtime to reconnect to recorded sessions and emit hints; IO piping not yet implemented.
- Added initial IO helpers `IoTarget`, `send` and `snapshot` CLI commands, and Python-side `docker exec tmux` command builders (`agents/src/orchestrator/io.py`); `just` wrappers not yet added.
- Tests: `agents/tests/test_io.py` covers command assembly (agent-marked).
- Added `just` wrappers `orchestrator-send` and `orchestrator-snapshot` for convenience.
- Next: wire tmux-based streaming/NDJSON transcripts with branch metadata, then validate via agent-marked tests.
