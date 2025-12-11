# Semantic-release Config Follow-ups

uid: FEAT-TOOLS-0001
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Category

FEATURE / TOOLS

## Current Situation

- Python semantic-release 9+ is configured in `pyproject.toml` with default changelog templates targeting `CHANGELOG.md` (Markdown output).
- Branch mapping now distinguishes releases vs prereleases: `main` does normal releases; `beta` emits prerelease tags with the token `beta.rc` (e.g., `vX.Y.Z-beta.rcN`).
- Release workflow relies on `uv run semantic-release version` / `publish` in CI; local checks can use `uv run semantic-release ... --noop` or `npx semantic-release --dry-run`.

## Suggested Improvements

- Adopt explicit changelog insertion flag (e.g., `<!-- version list -->`) to avoid template assumptions and reduce merge conflicts when the file is manually edited.
- Configure `mask_initial_release = false` if we want the first release notes to show real commits instead of a placeholder, or document the current masked behavior for clarity.
- Pin `changelog.mode = "update"` to ensure future template changes do not flip to `init` in edge cases (docs note both modes are valid).
- Add `environment.newline_sequence = "\n"` to enforce LF endings in generated files.
- Consider additional prerelease branches (e.g., `dev`, `staging`) with fixed tokens if needed; dynamic tokens that include branch/SHA are not supported and would require a wrapper script after `--noop`.
- Document a local dry-run recipe (`uv run semantic-release changelog --noop --stdout` and `uv run semantic-release version --noop --yes`) in `docs/ci.md` for contributors to validate changelog/tag generation without pushing.

## Notes / References

- Settings sourced from `python-semantic-release` docs (`changelog.default_templates.*`, `mode`, `mask_initial_release`, insertion flags, branch config).
- Current config already sets `default_templates.changelog_file`/`output_format` and adds a prerelease token for `beta`. Further changes above are pending review/approval.
