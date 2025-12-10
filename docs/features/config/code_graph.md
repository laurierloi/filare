# Code graph configuration

uid: FEAT-CLI-0015
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


## Summary

Define a YAML configuration that maps to `CodeGraphConfig` (root `pydantic.BaseModel`) with optional child configs for each supported tool: `CodeGraphPyDepsConfig`, `CodeGraphGrimpConfig`, and `CodeGraphPyan3Config`. CLI arguments merge with defaults to materialize this config before running any graph generation flow.

## Structure

- `GraphTool` (str, enum):
  - pydeps
  - grimp
  - pyan3
- `CodeGraphConfig` (root) includes:
  - `tool: GraphTool` (default is `grimp`).
  - `output_dir: Path` (default `outputs/code-graph`).
  - `format: str` (default depends on tool; e.g., `json` for grimp, `svg` for pydeps/pyan3).
  - `tools:` Optional nested configuration for each backend (`pydeps`, `grimp`, `pyan3`), each mapping to their respective child model.
- `CodeGraphPyDepsConfig` adds:
  - `max_bacon: int` / other pydeps-specific knobs.
  - `include_tests: bool`.
  - `graphviz_format: Literal[dot, svg]`.
- `CodeGraphGrimpConfig` adds:
  - `module_filter: Sequence[str]` to limit graph to certain packages.
  - `emit_dot: bool`.
  - `collapse_aliases: bool`.
- `CodeGraphPyan3Config` adds:
  - `group_by_module: bool`.
  - `no_undefined: bool`.
  - `exclude_paths: Sequence[Path]`.

## Usage

- CLI merges `CodeGraphConfig` with command-line flags (`--tool`, `--output`, `--format`); missing values fall back to defaults defined in `BaseModel`.
- When a config file (`code-graph.yml`) is present, the CLI loads it before merging CLI args.
- Each flow under `src/filare/flows/code_analysis/` accepts the resolved config and extracts its tool-specific section.
- YAML example:

```yaml
tool: grimp
output_dir: outputs/code-graph
format: json
tools:
  grimp:
    module_filter:
      - filare.render
    emit_dot: true
```

## Related

- CLI doc: `docs/features/cli/code_graph_config.md`.
