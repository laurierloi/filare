# CLI: `filare code` domain and `graph` subcommand scaffold

uid: FEAT-CLI-0009
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Add a Typer-powered `filare code` command (implemented in `src/filare/cli/code.py`) that hosts code-focused utilities. First child command: `filare code graph` with a pluggable `--tool` flag.

## Motivation

- Centralize code-analysis utilities under a consistent CLI namespace.
- Prepare for multiple graph generation backends without changing the UX.
- Enable both manual and CI refresh of code graphs from a single entrypoint.

## Proposal

- Create `src/filare/cli/code.py` Typer app and register it from the main CLI.
- Define `filare code graph --tool [pydeps|grimp|pyan3] [--output outputs/code-graph] [--format auto]`.
- Dispatch to flow helpers in `src/filare/flows/code_analysis/<tool>.py`, each exposing a `run(output_dir: Path, format: str, **kwargs)` returning emitted artifact paths.
- Ensure clear error when requested tool dependency is missing (friendly message + install hint).
- Write artifacts under `outputs/code-graph/` by default; allow override.

## Acceptance Criteria

- `uv run filare code graph --help` lists tool choices and defaults.
- Running with `--tool pydeps|grimp|pyan3` calls the correct flow and emits outputs in the chosen directory.
- Backward compatibility: existing CLI commands unchanged; Typer structure stays aligned with ongoing CLI migration.

## Notes

- Keep flags minimal; tool-specific options can be added later behind `--tool-arg` or similar.
- Respect repository instructions (no breaking CLI/scheme; use uv commands in docs/tests).

## Related Issues

- `docs/features/config/code_graph.md`
- `docs/features/cli/code_graph_config.md`
