# Basic Output Generation with Filare

## Purpose

Walk Persona A (technician) and Persona D (new engineer) through rendering a harness into HTML/PNG/SVG/TSV and seeing where outputs land.

## Prerequisites

- `uv venv; uv sync`
- Input harness YAML (e.g., `examples/demo01.yml`)
- Optional: component and metadata YAML files if you want to merge templates or metadata.

## Steps

1. Inspect available formats and flags: `uv run filare --help`
2. Render a harness with default formats: `uv run filare examples/demo01.yml -o outputs`
3. Change the base output name (if desired): `uv run filare examples/demo01.yml -O demo01_run1 -o outputs`
4. Generate and apply quantity multipliers (shared BOM scaling):
   - `uv run filare-qty tests/bom/bomqty.yml --multiplier-file-name outputs/quantity_multipliers.txt`
   - `uv run filare tests/bom/bomqty.yml --use-qty-multipliers --multiplier-file-name outputs/quantity_multipliers.txt -o outputs`
   - When prompted, enter the per-harness quantities (stored as JSON); reruns reuse the file unless `--force-new` is passed.

## Inputs

Minimal harness example:

```yaml
parts:
  connector_a:
    type: connector
    pins: [1, 2]
  connector_b:
    type: connector
    pins: [1, 2]
cables:
  cable1:
    length: 1m
connections:
  - from: connector_a.1
    to: connector_b.1
  - from: connector_a.2
    to: connector_b.2
```

## Commands

- Default render: `uv run filare examples/demo01.yml -f hpst -o outputs`
- With custom formats (HTML + PDF): `uv run filare examples/demo01.yml -f hP -o outputs`
- Force new multipliers: `uv run filare-qty tests/bom/bomqty.yml --force-new`

## Outputs

- HTML/PNG/SVG/TSV files in `outputs/` (or the input file’s directory if `-o` is omitted).
- `quantity_multipliers.txt` created or updated when running `filare-qty` (path configurable via `--multiplier-file-name`).
- Optional PDF bundle if format string includes `P`.

## Common Mistakes

- Using lowercase `p` when you wanted PDF (`P`), or uppercase `P` when you wanted PNG (`p`).
- Forgetting `-o` and wondering where files went (defaults to the input file’s folder).
- Passing format letters not listed in `--help`, leading to missing outputs.
- Running `filare-qty` but not passing `-u`/`-m` to `filare`, so multipliers are never applied.

## Troubleshooting

- “No such file” → check the harness path and that you are in the repository root.
- Missing expected format output → verify the `-f` letters and retry.
- Multiplier file not found → confirm `quantity_multipliers.txt` exists in the working directory or pass `-m/--multiplier-file-name` with the correct path.

## Related Features

- docs/ui/cli-help-review.md
- docs/issues/cli-help-defaults-and-examples.md
- docs/issues/filare-qty-help-context.md
