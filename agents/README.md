# Agents & Orchestrator Usage

This repo includes role guides (AGENT.*.md), prompt definitions, and orchestration tooling for running multiple agents via the codex container. Use this as a quick guide for the orchestrator flow by scenario.

## Common setup

- Build codex image if needed: `just codex-container-build`
- Prepare a manifest (e.g., `agents/manifest/test.yml`) with `id/role/branch/workspace/env_file/ssh_key`.
- Dry-run validate: `just orchestrator-validate manifest=agents/manifest/test.yml`
- Start sessions: `just orchestrator-start manifest=agents/manifest/test.yml [--execute]`
- Reconnect hints: `just orchestrator-resume-all`
- IO helpers: `just orchestrator-send container=<cid> session=<tmux> text="..."; just orchestrator-snapshot container=<cid> session=<tmux>`
- Feedback queue: `just orchestrator-feedback-list|add|resolve`
- Dashboard: `just orchestrator-dashboard [-- --json]`
- Agent tests (tooling only): `just orchestrator-test`
- Generate a task-specific manifest from a base defaults file:
  ```
  just orchestrator-generate-manifest \
    base=agents/manifest/example.yaml \
    output=outputs/agents/manifest-out.yml \
    role=FEATURE \
    branch=feat/123 \
    session_id=feat-123 \
    goal_file=goal.txt \
    context_file=ctx.txt \
    --issue docs/issues/ISS-0001.md
  ```
  Then: `just orchestrator-start manifest=outputs/agents/manifest-out.yml --execute`

## When implementing a feature

- Delegate to FEATURE agent:
  - Plan: `/orchestrator-plan`
  - Start: `/orchestrator-delegate-feature`
  - Track: `/orchestrator-status`
- If you need containerized agents, use a manifest with role `FEATURE` and start via `just orchestrator-start ... --execute`.
- Monitor logs/IO: `orchestrator-send/snapshot` as needed; resolve prompts via feedback commands.

## When fixing issues/bugs

- Delegate to FIXER or TOOLS (if tooling-related):
  - `/orchestrator-delegate-fixer` or `/orchestrator-delegate-tools`
  - Track with `/orchestrator-status`
- Use a manifest with the appropriate role and branch for isolated container runs; start with `--execute` if needed.
- Handle approvals via `orchestrator-feedback-*`; use dashboard to see pending prompts and session states.

## Project management / coordination

- For planning/backlog/status:
  - `/orchestrator-plan`, `/orchestrator-status`
  - `/orchestrator-delegate-project-manager` for deeper planning tasks
  - `just orchestrator-dashboard` to see running sessions and pending prompts
- Use `orchestrator-resume-all` to reconnect to running sessions across agents.

## Documentation / UI / Validation

- `/orchestrator-delegate-documentation`, `/orchestrator-delegate-ui`, `/orchestrator-delegate-validator` depending on the need.
- For containerized runs (e.g., UI or validation tasks needing isolation), define roles in the manifest and start via `orchestrator-start --execute`.
- Monitor via `orchestrator-send/snapshot` if interactive; resolve prompts via feedback commands.

## Tips

- Keep manifests current with correct SSH key/env file paths to avoid startup failures.
- Pass flags before the manifest when using `just orchestrator-start` (e.g., `just orchestrator-start manifest=... -- --execute` if you need extra args).
- Use `/codex-container-run` when you just need a raw shell inside the codex container (bind-mounted workspace).
- Avoid running agents directly on the host; prefer containers for isolation and reproducibility.
