# CLI Commands: page domain

uid: FEAT-CLI-0006
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Summary

Add `filare page <command>` to operate on a single page/sheet without full-document context, enabling faster iteration and targeted validation.

## Commands

- `filare page render <file>` — render one harness page to selected formats.
  - Input: single harness YAML file; optional metadata/components.
  - Flags: `-f, --formats <codes>`, `-c, --components <file...>`, `-d, --metadata <file...>`, `-o, --output-dir`, `-O, --output-name`, `--use-qty-multipliers`, `-m, --multiplier-file-name`.
  - Output: page-level artifacts (HTML/PNG/SVG/TSV/PDF as requested).
- `filare page preview <file>` — quick render to a temp location for visual check.
  - Input: single harness file.
  - Flags: `--format {html,png,svg}`, `--open` (attempt to open), `--keep` (retain temp output).
  - Output: temp render path; optional viewer open.
- `filare page info <file>` — summarize page metadata (sheet name, counts, cables/connectors).
  - Input: single harness file.
  - Flags: `--format {table,json}`, `--stats` (include counts/lengths).
  - Output: summary to stdout; JSON for automation.

## Inputs & Formats

- Single harness YAML plus optional metadata/component overlays.
- Format codes consistent with document domain.

## Outputs

- Rendered single-page artifacts; temp previews; info summaries.

## Rationale

- Persona A/D: rapid feedback loop for one page without bundling.
- Persona B: isolate issues per sheet; validate stats.
- Persona C: automation-friendly info command with JSON.

## Dependencies / Notes

- Built on Typer hierarchical CLI.
- Shares rendering pipeline with document commands; avoid duplicated logic.

## UI Notes

- Include quick-start examples for preview vs render, highlighting temp output location.
- Keep format letter meanings consistent with document commands and surface defaults.
- Provide `--format json` for `info` to support automation, while retaining readable tables.
