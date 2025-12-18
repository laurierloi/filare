# Session lifecycle management for orchestrated codex agents

uid: FEAT-TOOLS-0005
status: BACKLOG
priority: medium
owner_role: TOOLS
estimate: TBD
dependencies: [FEAT-TOOLS-0002, FEAT-TOOLS-0003, FEAT-TOOLS-0004]
risk: medium
milestone: backlog

## Summary

Add lifecycle controls that let the orchestrator start, monitor, pause, resume, and terminate multiple codex agent sessions in parallel. Each session maps to a container plus a running codex shell, with state tracked in a small registry for recovery and log capture.

## Motivation

- Ensure concurrent agents stay healthy and independent (no shared PTY confusion).
- Provide restart/cleanup paths when a session crashes or needs rotation.
- Enable future scheduling (priority queues) without manual docker fiddling.

## Proposal

- Define a `SessionRegistry` in `agents/src/orchestrator/runtime.py` that records container ID, state (`starting|running|paused|error|stopped`), start time, and transcript paths keyed by `session_id`.
- Launch path:
  1. Validate config (`FEAT-TOOLS-0004`), provision workspace/labels via `FEAT-TOOLS-0003`.
  2. Start a codex shell inside the container (optionally via `tmux new-session -s <id>` to allow non-interactive piping).
  3. Attach orchestrator-controlled IO channels (pipes or sockets) and mark state `running`.
- Control actions:
  - `pause` (prefer IO detach/tmux pause to avoid SIGSTOP side effects, but allow configurable stop signal if needed),
  - `resume` (reattach IO),
  - `restart` (stop + start),
  - `stop` (terminate codex process then container).
- Health checks: periodic `docker inspect` + optional heartbeat ping (send no-op command) to detect hung sessions; include retry/backoff policy and escalate to operator after N failures; auto-restart policy can be toggled per agent.
- Persist registry to `outputs/agents/<role>/<session-id>/state.json` for crash recovery.
- Track explicit git branch per session (from manifest) in the registry and enforce that sessions operate on the declared branch; surface mismatches as errors.

## Verification & Validation

- Start three sessions; verify registry tracks unique IDs and states transition `starting -> running`.
- Pause one session and confirm IO detaches while container remains; resume reattaches.
- Force-stop a container and ensure registry marks `error` and optional auto-restart works.
- After orchestrator restart, reload registry files and reconnect to surviving containers.
- Optional: add pytest coverage (marker `agent`) under `agents/tests/` that mocks docker to exercise state transitions, health check backoff/escalation, and branch tracking.

## Dependencies

- Uses container helpers from `FEAT-TOOLS-0003` and configs from `FEAT-TOOLS-0004`.
- IO routing defined in `FEAT-TOOLS-0006` and operator prompts in `FEAT-TOOLS-0007` rely on this lifecycle state.

## Progress / Notes

- Registry writes implemented in `agents/src/orchestrator/runtime.py` when planning/launching sessions; includes branch/workspace metadata and dry-run flag.
- CLI `start` and `resume-all` surface minimal lifecycle state; no pause/restart/health checks yet.
- Next: add state transitions beyond planned/running, heartbeat/backoff, and pause/resume hooks once IO layer is ready.
