# CLI: `filare code graph` configuration support

uid: FEAT-CLI-0011
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


## Summary

Allow `filare code graph` to consume a YAML configuration (mapped to `CodeGraphConfig`) while still honoring CLI flags. Store the resolved config in the flows under `src/filare/flows/code_analysis/` so each tool receives the right defaults and overrides.

## Motivation

- Some teams want persistent defaults (output dir, preferred format, filters) that survive CI runs.
- Centralizing config ensures `pydeps`, `grimp`, and `pyan3` all share a consistent schema.
- Keeps the CLI flexible: provide quick overrides via flags while persisting deeper options in YAML.

## Proposal

- Introduce `CodeGraphConfig` + tool-specific child models (see `docs/features/config/code_graph.md`).
- Add a `--config /path/to/code-graph.yml` option to `filare code graph`; if omitted, the CLI attempts to load `code-graph.yml` from the workspace root.
- Merge CLI args (`--tool`, `--output`, `--format`, extra tool flags) with config defaults before invoking the chosen tool flow.
- Provide helper `src/filare/flows/code_analysis/config.py` (or similar) to load and validate the config via Pydantic.
- CLI prints the resolved config (path + interpreted values) when run with `--verbose` or in debug mode.
- Document default file locations and required keys in the CLI help text.

## Acceptance Criteria

- `uv run filare code graph --config docs/code-graph.yml` loads the file, merges CLI overrides, and writes artifacts accordingly.
- Running without `--config` uses defaults from `CodeGraphConfig` defined in code (fallback to tool defaults).
- Tools read the rendered config and respect fields such as `module_filter`, `emit_dot`, etc.
- Config parsing errors surface as user-friendly messages.

## Related Issues

- `docs/features/config/code_graph.md`
- `docs/features/cli/code_command.md`
