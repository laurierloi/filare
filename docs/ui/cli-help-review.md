# Filare CLI Help Review (filare, filare-qty)

## Summary
The CLI help surfaces all flags but hides key defaults and workflows. Format codes are cryptic, multiplier handling is unclear, and there are no examples, so users have to infer how to run common tasks or how `filare-qty` fits into the flow.

## Usability Score
3/5 (Acceptable) — the help is present but the missing defaults, examples, and context force users to guess how to use core options.

## Observations
- `filare --help` lists flags but the only narrative is a single-line description; no examples or task framing for Persona A (technician) or Persona D (new engineer).
- Default formats are shown as `hpst`, but the option text does not expand those letters; the expansion appears later in the epilog and uses mixed casing (`p` vs `P`), which Persona D is likely to miss.
- Component/metadata files accept multiples, yet this is not explained; Persona B (systems) expects explicit mention of how multiple sources merge and in what order.
- Output directory defaulting to the first input file’s folder is not stated, so Persona C (automation) cannot predict where artifacts land.
- `--use-qty-multipliers` and `--multiplier-file-name` lack default values in the help; Persona B needs predictability, and Persona D needs to know when a file will be created or read.
- `filare-qty --help` has no command summary or workflow guidance; short flag `-f` here means “force” while `filare -f` means “formats,” creating cross-command cognitive load for Persona A/C.

## Pain Points
- Persona A: Cannot tell what `hpst` means or which one produces a picture; no example command to copy/paste.
- Persona B: Multiplier handling (defaults, location, when shared BOM scaling applies) is undocumented; multi-file ordering and output location are implicit.
- Persona C: Flag meanings vary between commands (`-f`), and there is no hint at non-interactive usage or expected exit behavior for CI.
- Persona D: Jargon (“shared bom”) and lowercase help text (“if set…”) provide no guidance or troubleshooting cues; missing “next step after filare-qty.”

## User Impact
Users must trial-and-error formats, multiplier files, and output locations, slowing onboarding and making automation brittle when defaults are not explicit.

## Error Message Evaluation
Not triggered in help flow; however, the help does not indicate what errors to expect when files are missing, when format codes are invalid, or when multiplier files are absent, leaving Personas A/B without actionable guidance.

## Default Behavior Evaluation
- Default formats: `hpst` (html, png, svg, tsv) not expanded next to the flag.
- Default output dir: first input file’s directory, unstated.
- Default multiplier file: `quantity_multipliers.txt`, unstated in both commands.
- Multi-file input order: sorted automatically, unstated (affects Persona B wanting deterministic bundling).

## Naming & Schema Issues
- Mixed-case format codes (`p` vs `P`) are easy to mistype; the letter codes do not match the file extensions (e.g., `g` → `gv`).
- Terminology shifts between `qty_multipliers`, `qty-multipliers`, and “shared bom” increase cognitive load.
- Short flag `-f` changes meaning between `filare` (formats) and `filare-qty` (force), creating mental context switching.

## Proposed Improvements
- Add a short “Common commands” block to both helps (e.g., `uv run filare examples/demo01.yml -f hpst -o outputs` and `uv run filare-qty tests/bom/bomqty.yml`).
- Show defaults inline: expand `hpst` in the option text, show `quantity_multipliers.txt` as the default path, and state the default output directory.
- Clarify workflow: indicate that `filare-qty` prepares multipliers for shared BOM scaling and that `--use-qty-multipliers` consumes them.
- Normalize wording and casing: sentence-case help, consistent “Qty multipliers” phrasing, and a clear table mapping format letters to extensions.
- Call out multi-file behavior: inputs are sorted; `-c/-d` accept multiples and are merged in order.

## Required Follow-Up (issues/features/rework)
- docs/issues/cli-help-defaults-and-examples.md
- docs/issues/filare-qty-help-context.md
- docs/workflows/basic-output-generation.md
