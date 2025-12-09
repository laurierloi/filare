# CLI: `filare code graph --tool grimp`

## Summary
Implement a grimp-based import graph generator that emits JSON (and optional DOT/SVG) for `filare`, exposed via `filare code graph --tool grimp`.

## Motivation
- Need a programmable graph representation for search/filter/highlighting in docs/UI.
- Grimp API provides module graph data without parsing DOT.

## Proposal
- Add dependency: `uv add --group dev grimp` (or optional import with guidance).
- Implement `src/filare/flows/code_analysis/grimp.py` with `run(output_dir: Path, format: str = "json") -> dict` that:
  - Builds the import graph for package `filare` via grimp.
  - Writes JSON nodes/edges to `outputs/code-graph/filare-imports-grimp.json`.
  - Optionally exports DOT/SVG when `format` requests it.
- CLI path: `filare code graph --tool grimp [--output ...] [--format json|dot|svg]`.
- Add smoke test to ensure JSON is emitted and has nodes/edges keys.

## Acceptance Criteria
- Command: `uv run filare code graph --tool grimp --output outputs/code-graph` writes JSON (and DOT/SVG when requested) with module ids.
- JSON schema documented minimally (nodes with id, edges with source/target) for UI consumers.
- Graceful missing-dep handling with install hint.

## Notes
- Output JSON should be stable/sortable to reduce diff noise in CI artifacts.
- Future: add `--module` filter to emit only neighbors; keep placeholder in flow signature if helpful.

## Related Issues
- `docs/features/config/code_graph.md`
- `docs/features/cli/code_graph_config.md`
