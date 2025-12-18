# Agent dashboard API/UI for orchestrated sessions

uid: FEAT-TOOLS-0009
status: BACKLOG
priority: low
owner_role: TOOLS
estimate: TBD
dependencies: [FEAT-TOOLS-0002, FEAT-TOOLS-0005, FEAT-TOOLS-0006]
risk: medium
milestone: backlog

## Summary

Design a minimal API/UI surface to list and inspect all running codex agent sessions, with future expansion toward an operator-friendly terminal emulator (tmux-backed) for interactive control.

## Motivation

- Provide a quick snapshot of session states, prompts, and health without diving into raw logs.
- Prepare for an optional interactive console where operators can jump into a session’s tmux pane.
- Keep this optional and low priority so core orchestration ships first.

## Proposal

- **API (minimal)**: expose a small HTTP or UNIX-socket JSON endpoint from the orchestrator process to return registry state (session ids, roles, states, uptime, pending prompts, log paths). Implementation can leverage `SessionRegistry` from `FEAT-TOOLS-0005`.
- **UI (minimal)**: start with a CLI view (`filare-agents dashboard --json|--table`) that renders the above data; no long-lived server required initially.
- **Future (tmux terminal)**: optional extension to spawn a multiplexed tmux layout per session and allow attaching via a single `just`/CLI command; uses IO routing from `FEAT-TOOLS-0006`.
- **Discovery**: add corresponding `just` shortcut (e.g., `just codex-orchestrator-dashboard`) and feed it through `scripts/generate_filare_agent_commands.py` so Codex extra commands stay in sync.

## Verification & Validation

- API/CLI returns a correct snapshot when multiple sessions are running; includes state, container id, workspace, and prompt counts.
- Dashboard command exits cleanly when no sessions exist (empty list).
- Optional tmux attach proves it can open a target session without impacting others.

## Notes

- Keep dependencies minimal (prefer standard library HTTP server if used); ensure no new runtime deps affect Filare core.
- Treat this as a low-priority/optional enhancement; prioritize lifecycle/IO plumbing first.
