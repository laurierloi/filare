# Shared manifest workspace allocation

uid: FEAT-TOOLS-0010
status: BACKLOG
priority: medium
owner_role: TOOLS
estimate: TBD
dependencies: [FEAT-TOOLS-0002, FEAT-TOOLS-0004]
risk: medium
milestone: backlog

## Summary

Support reusable manifest defaults and pattern-based workspace allocation so the orchestrator can spin up multiple agent sessions without manual path juggling. Key goals: reuse shared `.env`/SSH settings, auto-pick non-overlapping workspaces via templates/prefixes, and allow reuse of prior workspaces when desired.

## Proposal

- Manifest fields (per session):
  - `workspace_template`: e.g., `/tmp/filare-agent-{n}`; or `workspace_prefix` as shorthand (appends `{n}`).
  - `reuse_existing`: bool to allow reusing a previously recorded workspace for the same session/role if available.
  - Defaults for `env_file`/`ssh_key` remain in the `defaults` block; per-session override optional.
- Allocation logic:
  - On launch, if `workspace` does not exist and `workspace_template/prefix` is provided, orchestrator picks the lowest available `{n}` not in the registry for that role.
  - If `reuse_existing` is true and a stopped session with the same id/role exists, reuse its workspace path; otherwise pick a new one.
  - Only seed from repo when the chosen workspace is empty.
- Manifest generation helper:
  - CLI: `python -m orchestrator.generate_manifest --base agents/manifest/example.yaml --output outputs/agents/manifest-out.yml --role FEATURE --branch feat/123 --id feat-123 --goal-file goal.txt --issue docs/issues/ISS-0001.md ...`
  - Just wrapper: `just orchestrator-generate-manifest base=... output=... role=... branch=... session_id=... [goal_file=...] [context_file=...] [--issue <file> ...]`.
  - Reuses defaults (env/ssh/prefix) from the base, filling in session-specific fields and attaching context/issue files into metadata.
- Provide base manifest + derived manifests:
  - Base: shared defaults (`env_file`, `ssh_key`, optional `workspace_prefix`).
  - Derived: per-context files overriding `id/role/branch/goal` and optional `workspace_template`.
- CLI/just:
  - Keep using `just orchestrator-validate/start` with manifests; no UX change beyond optional new fields.

## Verification & Validation

- Given a template `/tmp/filare-agent-{n}` and existing sessions, launching two new sessions picks unique workspaces (e.g., `-1`, `-2`).
- When `reuse_existing` is true and a prior workspace exists, launch reuses it; when false, a new index is chosen.
- Agent tests cover template resolution and registry-based allocation.

## Progress / Notes

- Added manifest fields `workspace_template`, `workspace_prefix`, and `reuse_existing` to `AgentSessionConfig`; allocation helper in `agents/src/orchestrator/workspace.py` picks next free slot based on registry.
- Tests updated to cover template-based workspace resolution.
- Next: expose sample base/derived manifests and refine reuse policy (stopped vs running); consider auto-populating `workspace` when omitted.
