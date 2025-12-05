# Quantity Multipliers (Current Workflow)

## Purpose

Guide users through creating and applying quantity multipliers using the existing `filare-qty` + `filare -u` flow.

## Prerequisites

- `uv venv; uv sync`
- Harness YAML file(s)
- Terminal access (no GUI required)

## Steps

1. Generate multipliers file: `uv run filare-qty tests/bom/bomqty.yml`
2. Inspect/edit `quantity_multipliers.txt` as needed.
3. Render harnesses with multipliers applied: `uv run filare examples/demo01.yml -u -m quantity_multipliers.txt -o outputs`

## Inputs

- Harness YAML files (e.g., `examples/demo01.yml`)
- Optional existing `quantity_multipliers.txt`

## Commands

- Create/update multipliers: `uv run filare-qty <files...> [-m quantity_multipliers.txt] [-f]`
- Apply during render: `uv run filare <files...> -u -m quantity_multipliers.txt -o outputs`

## Outputs

- `quantity_multipliers.txt` in working directory (default)
- Rendered outputs (HTML/PNG/SVG/TSV/PDF) in `outputs/` or input directory

## Common Mistakes

- Forgetting `-u` when rendering, so multipliers are ignored.
- Misplacing `quantity_multipliers.txt` (command defaults to working directory).
- Using `-f` meaning different things: force in `filare-qty`, formats in `filare`.

## Troubleshooting

- “file not found” for multipliers → pass `-m` with the correct path.
- Missing scaled counts → ensure `-u` is set and multipliers file has matching keys.

## Related Features

- docs/features/integrated-quantity-management.md
- docs/issues/quantity-workflow-integration.md
