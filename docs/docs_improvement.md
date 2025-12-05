# Documentation Improvements (tracker)

Use this page to track Filare documentation gaps discovered in code or workflows. Each entry lists the target doc location and the source of truth in code/tests.

## Open gaps

- Document representation and hash guard  
  - Document the `DocumentRepresentation` YAML (`*.document.yaml`), hash tracking (`document_hashes.yaml`), and `allow_override` flag described in README container notes. Source: `src/filare/models/document.py`, `src/filare/flows/build_harness.py`. Target: `docs/architecture.md` or a dedicated `docs/document_representation.md`.
- Quantity multipliers end-to-end workflow  
  - Expand beyond the quickstart to cover `filare-qty` prompts, `--use-qty-multipliers`, multiplier file placement, and shared BOM scaling across multiple harnesses. Source: `src/filare/models/harness_quantity.py`, `src/filare/cli.py`, tests under `tests/models/test_harness_quantity.py` and `tests/test_harness_quantity_cli.py`. Target: `docs/syntax.md` (options) and `docs/workflows/basic-output-generation.md`.
- Cut/termination page usage example  
  - Add a minimal harness YAML demonstrating `options.include_cut_diagram` / `options.include_termination_diagram` with expected outputs and caveats. Source: `src/filare/pages.py`, `src/filare/flows/build_harness.py`, and rendering stubs. Target: `docs/pages.md` and a small example under `tests/rendering/`.
- Agent system overview (added in `docs/agents.md`)  
  - Keep this file updated when agent roles/rules change in `AGENTS.md` and `agents/AGENT.*.md`.
