# Operator feedback loop for orchestrated agents

uid: FEAT-TOOLS-0007
status: BACKLOG
priority: medium
owner_role: TOOLS
estimate: TBD
dependencies: [FEAT-TOOLS-0002, FEAT-TOOLS-0005, FEAT-TOOLS-0006]
risk: medium
milestone: backlog

## Summary

Provide a structured way for running codex sessions to request operator input (approvals, credentials, strategic choices) and for the orchestrator to inject those responses back into the correct agent stream.

## Motivation

- Keep multi-agent runs safe by pausing for approval on risky operations (network, destructive commands).
- Ensure operator context (which agent, which workspace, why) accompanies every prompt.
- Allow asynchronous operation: agent can continue others while waiting for operator.

## Proposal

- Add a `PromptQueue` in `agents/src/orchestrator/feedback.py` backed by a small JSON file per session plus an aggregate queue.
- Standardize prompt payload: `session_id`, `role`, `workspace`, `branch`, `reason`, `requested_action`, `suggested_reply`, `severity`, `created_at`.
- When an agent hits an approval boundary (e.g., tries to run networked command), it emits a `requires_operator` message via IO layer (`FEAT-TOOLS-0006`), which the orchestrator intercepts and places in the queue.
- Allow per-session policy to auto-allow certain categories (e.g., network or destructive commands) when configured in the manifest/operator policy, so isolated environments can bypass manual approval while still logging the decision.
- Provide two handling paths:
  - **CLI-driven**: `filare-agents feedback list|approve|reject --session <id>` prints context and pipes reply back via `send_message`.
  - **Notify hook**: optional webhook/email/stdout notifier for pending prompts (implementation optional now; spec should allow plugging one later).
- Once answered, orchestrator logs the decision and attaches it to the session transcript; default behavior resumes the paused session.

## Verification & Validation

- Simulate a prompt insertion and confirm it appears in the queue with metadata.
- Approve via CLI; verify response is injected and session transitions from `paused` to `running`.
- Reject path should send a clear message to the agent and keep logs consistent.
- Pending prompts should survive orchestrator restart (persisted queue).
- Optional: add pytest (marker `agent`) under `agents/tests/` that exercises queue persistence, approve/reject flows, and branch/role metadata in prompt payloads.

## Dependencies

- Relies on session state (`FEAT-TOOLS-0005`) and message routing (`FEAT-TOOLS-0006`).
- CLI plumbing provided in `FEAT-TOOLS-0008`.

## Progress / Notes

- Not yet implemented; pending IO routing and session lifecycle hooks. Plan to respect per-session policy for auto-allowing network/destructive actions while logging decisions.
