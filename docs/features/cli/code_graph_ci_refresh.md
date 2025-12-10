# CI: refresh code graphs via `filare code graph`

uid: FEAT-CLI-0010
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


## Summary

Add a CI job to run `filare code graph` and publish artifacts (JSON/DOT/SVG) for the selected tools, keeping graphs current and downloadable.

## Motivation

- Ensure code graph outputs stay in sync with code changes.
- Provide downloadable artifacts for reviewers without running tools locally.

## Proposal

- CI job (GitHub Actions) runs after tests, using repo venv and uv commands.
- Steps:
  1. `uv run filare code graph --tool grimp --output outputs/code-graph` (JSON primary).
  2. Optionally run `--tool pydeps` and `--tool pyan3` when dependencies available (can be matrix or conditional).
  3. Upload `outputs/code-graph/**/*` as an artifact; optionally commit to `gh-pages` if desired.
- Job should fail fast with clear logs if a tool is missing; allow toggling tool list via matrix/inputs.
- Keep runtime reasonable by scoping to `src/filare` and avoiding expensive formats.

## Acceptance Criteria

- CI pipeline produces artifacts for at least the JSON import graph (grimp) on every push/PR.
- Logs show the exact command invocations; failures mention missing deps plainly.
- No changes to existing test or release jobs; this is additive.

## Notes

- Reuse the same CLI entrypoint as local users; avoid bespoke scripts.
