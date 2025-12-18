# Codex orchestrator for parallel agent sessions

uid: FEAT-TOOLS-0002
status: BACKLOG
priority: medium
owner_role: TOOLS
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Design a lightweight orchestration layer that uses the codex-ready container (`docker/Dockerfile.codex` + `just codex-container-*`) to run multiple Filare agent sessions in parallel. The orchestrator should provision per-agent workspaces, launch codex shells under matching roles, route stdin/stdout for each session, and provide hooks for operator feedback/approvals. All logic stays outside Filare runtime behavior and lives under `src/filare/agents/` as a Python library plus a thin CLI.

## Motivation

- Parallelize multi-agent workstreams (feature/fix/docs/test) without manual terminal management.
- Standardize how agent containers are started/configured (SSH keys, `.env`, workspace seed) so downstream harnesses can rely on predictable behavior.
- Provide structured IO so an ORCHESTRATOR agent can script interactions, capture transcripts, and request operator input when needed.

## Proposed Flow

1. **Image availability**: Build/update the codex image via `just codex-container-build` (uses `docker/Dockerfile.codex`).
2. **Agent configuration**: Declare agent manifests (role, goal, workspace path, env file, SSH key, resource limits, operator escalation policy).
3. **Session launch**: Start each agent via `just codex-container-run` or a Python wrapper that calls `scripts/run_codex_container.sh`, binding per-agent workspace and `.codex` cache; optionally wrap in `tmux` panes for supervision.
4. **IO routing**: For each session, maintain non-interactive pipes (stdin/stdout/stderr) and a small control socket/API to send instructions and collect logs; store transcripts under `outputs/agents/<role>/<session-id>/`.
5. **Operator feedback loop**: Allow the orchestrator to pause an agent with a prompt, surface a summarized question to the operator, then inject the response back into the session.
6. **Lifecycle**: Support start/stop/restart, health checks (container alive, codex responsiveness), and cleanup (workspace sync optional).
7. **CLI wrapper**: Provide `uv run filare-agents ...` commands for manual kicks (list agents, start/stop, tail logs) that delegate to the library.
8. **Tasking via `just`**: Add orchestration-focused `just` recipes that wrap the CLI (e.g., start/stop/tail/feedback) so human operators have one-touch entrypoints; update `agents/extra_commands.yml` to mirror new recipes for Codex hints. Avoid duplicating command definitions—reuse the `scripts/generate_filare_agent_commands.py` flow that already compiles `just` targets into agent command metadata, and keep agent-specific recipes inside `agents/justfile` (with root wrappers for generation).

## Acceptance / Validation Outline

- Running the orchestrator against two+ agent manifests launches distinct containers with isolated workspaces and `.codex` caches.
- Commands can send text to a specific agent and receive streamed output/logs without cross-talk.
- Operator prompts are surfaced with clear session metadata and are injectible back into the correct agent.
- Shutdown cleans containers and temporary SSH mounts; no leaked processes remain.

## Progress / Notes

- Implemented initial orchestrator skeleton under `agents/src/orchestrator/` with manifest validation, dry-run container launch planning, registry writes, and `resume-all` planning. Added Typer CLI commands `validate`, `start`, and `resume-all`, plus `just` wrappers for quick invocation.
- Added agent-marked tests under `agents/tests/` for manifest parsing and registry/command assembly (opt-in via `-m agent`).
- Next: integrate IO routing, operator prompts, labels for container discovery, and expand `just` wrappers once the CLI stabilizes.
- Created a standalone `agents/pyproject.toml` and `agents/justfile` for orchestrator tooling to keep dependencies isolated from Filare runtime.
- Root `justfile` now imports `agents/justfile`; orchestrator and codex container recipes live under agents while top-level wrappers remain available for command generation.

## Dependencies and Interactions

- Uses `docker/Dockerfile.codex` and `scripts/run_codex_container.sh` as the runtime base.
- Builds on `just codex-container-build|run|sh` tasks as entrypoints.
- New library/CLI would live under `src/filare/agents/` and must avoid touching Filare runtime logic.

## Open Points to Resolve

- Decide whether to store per-agent config in YAML vs JSON (default to YAML under `configs/agents/*.yml`).
- Choose IO transport inside container (plain PTY via `docker exec -it`, named pipes, or tmux piping); target minimal dependencies.
- Define transcript retention/rotation strategy to avoid bloated `outputs/`.
- Determine the exact set of new `just` targets and corresponding `agents/extra_commands.yml` entries to keep operator UX aligned with orchestrator CLI, without double-defining commands already emitted by `scripts/generate_filare_agent_commands.py`.
- Clarify the split between root just wrappers (for command generation) and agent-local recipes in `agents/justfile`.
