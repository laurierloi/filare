# Ruff pre-commit hook setup

## Category

TOOLS

## Evidence

- `docs/tasks.md` lists `230727GTW1_setup_ruff_pre_commit` without a corresponding tracker.
- Repo currently uses black/isort/pre-commit; Ruff adoption status is unclear.

## Expected Outcome

- Clear decision on adopting Ruff (lint/type-check overlap) in pre-commit, with configuration documented if enabled.

## Proposed Next Steps

1. Check current lint tooling in `pyproject.toml`/pre-commit config for Ruff presence.
2. If adding Ruff, document config (rules, ignores), update pre-commit hooks, and add CI note.
3. If deferring, record rationale and remove the task from legacy lists.

## Related Items

- `docs/tasks.md` tooling tasks.
