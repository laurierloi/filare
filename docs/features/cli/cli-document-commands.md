# CLI Commands: document domain

uid: FEAT-CLI-0001
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Add `filare document <command>` to manage full-document outputs (HTML/PDF bundles, title pages) and inspect render configuration.

## Commands

- `filare document render <files...>` — render full documents (multi-page) with optional title page and PDF bundle.
  - Input: harness YAML files; optional metadata/components.
  - Flags: `-f, --formats <codes>` (e.g., hpstP), `-c, --components <file...>`, `-d, --metadata <file...>`, `-o, --output-dir`, `-O, --output-name`, `--no-titlepage`, `--pdf-bundle`, `--use-qty-multipliers`, `-m, --multiplier-file-name`.

## Implementation Assessment (2025-02-04)

- Current support: No `document` Typer group; `filare run` renders harness outputs and titlepage but not scoped document subcommands.
- Clarity: Inputs/flags match existing `render` command; wiring to a new Typer group is straightforward.
- Difficulty: Medium — reuse existing render flow and bundle helpers; needs CLI plumbing and tests.
  - Output: HTML/PNG/SVG/TSV/PDF artifacts; console summary of outputs.
- `filare document inspect <file>` — show document-level options (page sizes, fonts, metadata applied).
  - Input: single harness file (or merged metadata file).
  - Flags: `--format {table,json}`, `--include-defaults`.
  - Output: structured summary to stdout.
- `filare document bundle <files...>` — bundle existing rendered pages into a PDF.
  - Input: paths to rendered page files.
  - Flags: `-o, --output <path>`, `--order <file...>` (explicit ordering).
  - Output: combined PDF and ordering report.

## Inputs & Formats

- Harness YAML files plus optional metadata/component YAMLs.
- Format codes mirror existing ones; defaults surfaced inline.

## Outputs

- Rendered artifacts in chosen formats; bundle outputs; inspection summaries.

## Rationale

- Persona A/D: clear, task-scoped render command with explicit defaults.
- Persona B: deterministic ordering and bundling controls.
- Persona C: predictable exit codes and machine-readable inspection outputs.

## Dependencies / Notes

- Works with hierarchical CLI and Typer migration.
- Share format code table across domains to avoid conflicts.

## UI Notes

- Show default format codes and expand them inline (`hpstP`) plus an example per common task (HTML+PDF, custom output name).
- Clarify output locations (default input dir vs `-o`) and bundling order rules.
- Provide machine-readable inspection output (`--format json`) while keeping table output concise for technicians.
