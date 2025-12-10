# CLI: `filare code graph --tool pydeps`
uid: FEAT-CLI-0014
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Implement the pydeps-based import graph generator, wired to `filare code graph --tool pydeps`, producing DOT/SVG (and optionally JSON) import graphs for the `filare` package.

## Motivation

- Quick, visual module import graph to spot coupling/cycles.
- Uses a mature tool (`pydeps`) with Graphviz output, familiar to developers.

## Proposal

- Add dependency: `uv add --group dev pydeps graphviz` (or gate with optional import and error message).
- Implement `src/filare/flows/code_analysis/pydeps.py` with a `run(output_dir: Path, format: str = "svg") -> dict` that:
  - Calls pydeps programmatically (or via `uv run pydeps` fallback) on `filare` package.
  - Writes DOT to `outputs/code-graph/filare-imports-pydeps.dot` and renders SVG when format supports it.
  - Returns emitted paths for CLI to print.
- CLI path: `filare code graph --tool pydeps [--output ...] [--format dot|svg]`.
- Add smoke test that calls the flow with a temp output dir and asserts files exist (skip if Graphviz unavailable).

## Acceptance Criteria

- Command succeeds locally: `uv run filare code graph --tool pydeps --output outputs/code-graph` produces DOT (+SVG when `dot` available).
- Friendly error if pydeps/Graphviz missing (no stack trace; include install hint via uv).
- Outputs live under the requested directory; filenames include `pydeps` to avoid clashes.

## Notes

- Keep default scope to `src/filare` to avoid test/template noise.
- Preserve backward compatibility; no changes to render/BOM behavior.

## Related Issues

- `docs/features/config/code_graph.md`
- `docs/features/cli/code_graph_config.md`
