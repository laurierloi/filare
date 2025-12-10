# CLI Commands: drawio domain

uid: FEAT-CLI-0002
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


## Summary

Add `filare drawio <command>` to manage Draw.io integrations, keeping diagram assets in sync with Filare harness data.

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
