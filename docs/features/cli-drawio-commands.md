# CLI Commands: drawio domain

uid: FEAT-CLI-0002
status: IN_PROGRESS
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Add `filare drawio <command>` to manage Draw.io integrations, keeping diagram assets in sync with Filare harness data.

## Requirements
- Provide `filare drawio` group with `import`, `export`, `sync`, `validate`, `edit`, and `review` subcommands and listed flags/options.
- Support Draw.io (.drawio/.xml) inputs plus YAML/JSON mapping/rules; harness YAML for export/sync.
- Emit human-readable and JSON outputs for validation/sync reports; keep backward compatibility with existing harness rendering.
- Honor CLI > ENV > CONFIG > DEFAULT precedence where settings apply; use `pathlib` for all paths.
- Ensure non-interactive-friendly behaviors (backups, dry-run) for CI workflows.

## Commands

- `filare drawio import <file>` — import a Draw.io diagram and map nodes to Filare components.
  - Input: Draw.io file (.drawio or .xml); optional mapping YAML.
  - Flags: `--mapping <path>` (component pin mapping), `--output <path>` (save mapped YAML), `--dry-run`.
  - Output: mapped YAML/components to file/stdout; report of matched/unmatched nodes.
- `filare drawio export <harness.yml>` — generate a Draw.io diagram from a harness.
  - Input: harness YAML.
  - Flags: `--template <drawio file>`, `--output <path>`, `--style <json|yaml>` (styling rules).
  - Output: Draw.io file; console summary of elements generated.
- `filare drawio sync <harness.yml> <diagram.drawio>` — bidirectional sync to update labels/pins.
  - Input: harness YAML and existing Draw.io file.
  - Flags: `--direction {to-drawio,to-harness,bidirectional}`, `--backup <path>`, `--report <path>` (JSON summary).
  - Output: updated file(s); sync report (JSON/text); backups when requested.
- `filare drawio validate <diagram.drawio>` — check Draw.io file for required shapes/labels.
  - Input: Draw.io file.
  - Flags: `--rules <path>` (validation rules), `--format {table,json}`.
  - Output: validation summary; exit code for CI.
- `filare drawio edit <diagram.drawio>` — open Draw.io for interactive editing.
  - Input: Draw.io file.
  - Flags: `--editor <cmd>` (override drawio binary), `--no-validate` (skip post-edit validation), `--rules <path>` (optional validation rules).
  - Output: exit code based on optional validation.
- `filare drawio review <diagram.drawio>` — open Draw.io read-only, collect CLI comments, and save to a file.
  - Input: Draw.io file.
  - Flags: `--comments-path <path>` (required output), `--rules <path>` (optional validation), `--format {table,json}` for the validation summary.
  - Output: validation report (if run), saved comments file, exit code.

## Inputs & Formats

- Draw.io files plus optional mapping/rules in YAML/JSON.
- Harness YAML for export/sync.

## Outputs

- Generated/updated Draw.io files; mapping YAML; validation and sync reports (text/JSON).

## Rationale

- Persona A/D: easier to bring existing diagrams into Filare or export visuals.
- Persona B: validation and sync reports improve traceability.
- Persona C: JSON reports enable CI checks for diagram consistency.

## Dependencies / Notes

- Built on Typer hierarchical CLI.
- Requires defined mapping/validation rule schemas and Draw.io parsing utilities.

## UI Notes

- Provide before/after and direction (`to-drawio`, `to-harness`) examples, plus default file locations.
- Keep reports available as both tables and JSON; highlight backup/restore flags prominently.
- Surface mapping/rules schema references to reduce trial-and-error.

## Steps
- [x] Map existing drawio tooling (if any) and define schema/IO helpers needed for import/export/sync/validate/edit/review.
- [x] Implement reusable Draw.io parsing/mapping utilities (load, merge mappings/rules, apply direction flags, backups/dry-run, editor invocation, comment capture).
- [x] Add Typer `drawio` subcommands with required flags, outputs (table/JSON), and exit codes; ensure pathlib usage.
- [x] Add tests covering import/export/sync/validate behaviors, edit (editor stub + optional validation), review (read-only + comment capture), dry-run/backup, and JSON report outputs.
- [x] Update docs/help/examples to reflect new drawio commands, flags, and default paths.

## Progress Log
2025-12-10: Drafted plan, set status to IN_PROGRESS; awaiting operator review before implementation.
2025-12-10: Implemented placeholder Draw.io CLI commands (import/export/sync/validate/edit/review) with tests; docs updates pending.
2025-12-10: Resolved rebase conflicts and wired metadata/drawio CLIs; tests passing.
2025-12-10: Documented drawio CLI usage and examples; marked docs step complete.

## Implementation
- [ ] Audit current Draw.io support and identify reuse vs new helpers (file loading, mapping/rules schema, direction handling).
- [ ] Design data flow for import/export/sync/validate/edit/review (IO formats, backups, dry-run, JSON reports, editor invocation, comment capture) with pathlib paths.
- [ ] Implement helper layer plus Typer `drawio` subcommands wired to these helpers.
- [ ] Add focused tests for each subcommand including report formats, safety flags, and edit/review flows.
- [ ] Refresh docs/help examples to match new CLI behaviors.
