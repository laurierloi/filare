# CLI: `filare code graph --tool pyan3`

uid: FEAT-CLI-0013
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Implement a pyan3-based static call graph generator exposed via `filare code graph --tool pyan3`, producing module-grouped call graphs (DOT/SVG) for Filare.

## Motivation

- Understand call relationships and entrypoints beyond imports.
- Useful for debugging flows and assessing impact of changes.

## Proposal

- Add dependency: `uv add --group dev pyan3 graphviz` (or optional import with hint).
- Implement `src/filare/flows/code_analysis/pyan3.py` with `run(output_dir: Path, format: str = "svg") -> dict` that:
  - Runs pyan3 on `src/filare/**/*.py` with grouping and no function bodies inlined.
  - Emits DOT to `outputs/code-graph/filare-callgraph-pyan3.dot` and renders SVG when Graphviz available.
- CLI path: `filare code graph --tool pyan3 [--output ...] [--format dot|svg]`.
- Add smoke test exercising the flow with temp output dir; skip gracefully if Graphviz missing.

## Acceptance Criteria

- Command succeeds: `uv run filare code graph --tool pyan3 --output outputs/code-graph` emits DOT (+SVG when `dot` is available).
- Clear error if dependency missing; no stack trace.
- Output filenames distinguish pyan3 to avoid collision with pydeps outputs.

## Notes

- Static call graphs can be noisy; keep defaults conservative (grouped, no colors, limit size if needed).

## Related Issues

- `docs/features/config/code_graph.md`
- `docs/features/cli/code_graph_config.md`
