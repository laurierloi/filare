# Agent Guide

This page summarizes how Filare’s multi-agent workflow is configured and what each role owns. For full rules, see `AGENTS.md` and the role playbooks under `agents/AGENT.<ROLE>.md` in the repository root.

## Configuration

- **Base rules**: `AGENTS.md` defines shared constraints (uv-only commands, backward-compatible CLI/schema, docs/tests expectations, branch naming `<role>/<feature>`, MR target `beta`, and output paths for plans under `outputs/agents/<role>/plan-N`).
- **Role rules**: Each role has a strict guide in `agents/AGENT.<ROLE>.md`. Follow both the base guide and your role guide.
- **Workflow**: Ask for your role, read the guides, write a short step plan, implement/test/docs, then open a PR into `beta`. Keep changes scoped to your role (e.g., DOCUMENTATION cannot alter behavior).
- **Tooling**: Use `uv venv`, `uv sync`, and `uv run …` for all Python commands; avoid raw `pip`/`python`. Generated outputs should live under `outputs/` or temp dirs as noted in `AGENTS.md`.

## Roles (overview)

- **DOCUMENTATION** (`agents/AGENT.DOCUMENTATION.md`): Improve user/dev docs and docstrings; may add tests only to validate doc examples; no behavior changes.
- **FEATURE** (`agents/AGENT.FEATURE.md`): Implement one scoped feature per branch, track progress in `docs/features/<feature>.md`, add tests/docs, maintain compatibility unless explicitly allowed.
- **REWORK** (`agents/AGENT.REWORK.md`): Refactor and improve structure/clarity without altering user-visible behavior or schema.
- **COVERAGE** (`agents/AGENT.COVERAGE.md`): Increase test coverage with focused pytest/YAML regressions; document dead code; no feature work.
- **TOOLS** (`agents/AGENT.TOOLS.md`): Maintain CI, build scripts, Docker/tooling, and docs build pipeline; never touch runtime behavior.
- **UI** (`agents/AGENT.UI.md`): Evaluate usability and produce reports/workflows; does not change code or docs beyond reports/issues.
- **EXPLORATOR** (`agents/AGENT.EXPLORATOR.md`): Conduct research only; produce reports under `docs/research/`; no code/doc changes.
- **JUDGE** (`agents/AGENT.JUDGE.md`): Review and approve/reject other agents’ branches; outputs are reviews/issues only.
- **VALIDATOR** (`agents/AGENT.VALIDATOR.md`): Write acceptance/functional tests to verify behavior against specs; no code or doc changes beyond tests/issues.
