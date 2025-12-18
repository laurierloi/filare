# Agent manifest schema for orchestrated codex sessions

uid: FEAT-TOOLS-0004
status: BACKLOG
priority: medium
owner_role: TOOLS
estimate: TBD
dependencies: [FEAT-TOOLS-0002]
risk: medium
milestone: backlog

## Summary

Define a declarative manifest for each agent session so the orchestrator can consistently supply role, goals, workspace, env/SSH bindings, and operator contact rules. Manifests live under `configs/agents/*.yml` and are parsed by the `src/filare/agents` library before container launch.

## Motivation

- Centralize per-agent configuration instead of embedding flags in scripts.
- Allow reproducible multi-agent runs (e.g., FEATURE agent + VALIDATOR agent) with the same inputs.
- Encode operator escalation preferences up front to avoid blocking mid-run.

## Proposal

- YAML structure (`AgentSessionConfig`): `id`, `role`, `goal`, `workspace`, `env_file`, `ssh_key`, optional `image`, `resources` (CPU/mem hints), `mounts`, `startup_script`, `operator_contact` (e.g., requires_approval_for: [network, destructive_cmds]), `transcript_dir`, and `tags`.
- Provide schema validation with `pydantic`-style model (no runtime change to Filare core) in `agents/src/orchestrator/config.py` (or equivalent sub-repo style layout).
- Support manifest bundles listing multiple agents plus shared defaults (e.g., default env file) that get merged.
- Allow override via CLI flags (`--workspace`, `--goal`, `--env-file`) to simplify ad-hoc runs.
- Require explicit git branch selection per agent (e.g., `branch` field) so each session is pinned to a known branch; orchestrator should refuse to launch if branch is missing.
- Store only references to sensitive files (SSH key paths), never inline secrets; provide sample manifests under `configs/agents/demo.yml` as a starting point.

## Verification & Validation

- Load a manifest with missing required fields and confirm clear validation errors.
- Load a bundle of two agents sharing defaults; resulting configs should differ only where overridden.
- Round-trip: serialize parsed config back to YAML for logging and ensure no data loss.
- Optional: add schema pytest coverage under `agents/tests/` gated by `-m agent` to validate required fields (including `branch`) and bundle merging.

## Dependencies

- Builds on `FEAT-TOOLS-0002` (overall orchestrator design) and feeds launch helpers in `FEAT-TOOLS-0003`.
- Upstream consumers: session lifecycle (`FEAT-TOOLS-0005`) and IO routing (`FEAT-TOOLS-0006`).

## Progress / Notes

- Implemented manifest loader/validator in `agents/src/orchestrator/config.py` with required fields (`id`, `role`, `branch`, `workspace`, `env_file`, `ssh_key`) and default merging.
- Added agent-marked tests (`agents/tests/test_config.py`) covering defaults, duplicate detection, and missing branch errors.
- Added a gitignored sample manifest at `agents/manifest/test.yml` for local dry-run/testing.
- Next: document sample manifest under `configs/agents/demo.yml` and extend schema for operator policy defaults.
