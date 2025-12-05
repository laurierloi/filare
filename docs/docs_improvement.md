# Documentation Improvements (tracker)

Use this page to track Filare documentation gaps discovered in code or workflows. Each entry lists the target doc location and the source of truth in code/tests.

## Open gaps

- Quantity multipliers syntax reference  
  - Add a short subsection to `docs/syntax.md` under options explaining `--use-qty-multipliers`/`--multiplier-file-name`, expected `quantity_multipliers.txt` shape, and when to run `filare-qty`. Source: `src/filare/models/harness_quantity.py`, `src/filare/cli.py`.
- Cut/termination regression example  
  - Add a small YAML in `tests/rendering/` that exercises `include_cut_diagram` and `include_termination_diagram`, then cross-link from `docs/pages.md` once stabilized.
- Agent system upkeep (docs/agents.md)  
  - Keep the agent overview aligned with changes to `AGENTS.md` and `agents/AGENT.*.md` (e.g., new roles or workflow adjustments).

## Completed this round

- Document representation and hash guard behavior (added to `docs/architecture.md`).
- Quantity multiplier workflow walkthrough (updated `docs/workflows/basic-output-generation.md`).
- Cut/termination page usage example (added to `docs/pages.md`).
- Agent system overview scaffold (added `docs/agents.md`).
