# Document filare-qty CLI usage
uid: ISS-0008
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

The quantity multiplier helper (`filare-qty`) is not documented anywhere alongside the primary CLI.

## Category

DOCUMENTATION

## Evidence

- README.md:220-255 and docs/README.md:208-243 only describe the `filare` CLI; `filare-qty` (exposed via `pyproject.toml`) is not mentioned anywhere in the user-facing docs.
- `rg "filare-qty" docs README.md` returns no matches, so users have no guidance on the quantity multiplier helper CLI that AGENTS.md calls out as stable.

## Suggested Next Steps

1. Add a short section introducing `filare-qty`, what it computes (quantity multipliers/BOM scaling), and when to use `--use-qty-multipliers`, linking to an example YAML (e.g., `tests/bom/bomqty.yml`).
2. Provide a basic invocation example using the uv workflow (`uv run filare-qty <file>.yml`) and clarify expected outputs.
3. Cross-link this section from the main README and docs landing page so users discover the secondary CLI.
