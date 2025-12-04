# CLI Subcommand Ergonomics

## Summary
Filare exposes two entrypoints (`filare`, `filare-qty`) but does not present them as related subcommands or cross-reference them. Discovery is weak, flag semantics diverge, and there is no overview of when to use each tool, leaving users to guess how quantity workflows fit into rendering.

## Usability Score
2/5 (Poor) — commands work but are not discoverable as a cohesive CLI, increasing cognitive load and mistakes.

## Observations
- `filare --help` never mentions `filare-qty`, so users do not learn that quantity preparation is a separate command.
- There is no `filare qty` subcommand or alias; the tools feel unrelated despite sharing outputs (shared BOM scaling).
- Flag semantics diverge (`-f` = formats vs force), and defaults are hidden (multiplier filename, output dir), so users cannot transfer knowledge between commands.
- No listing of available commands; `project.scripts` defines two executables, but only doc hunting reveals the second.
- Workflow is implicit: users must infer that `filare-qty` should run before `filare -u`.

## Pain Points
- Persona A: Misses the quantity step entirely; sees only `filare` help and never learns about multipliers.
- Persona B: Cannot design deterministic automation without a documented command map or default paths.
- Persona C: Has to special-case flag meanings between executables; lack of `filare qty` subcommand complicates scripting conventions.
- Persona D: Has no guided flow; the separate executable feels like a different tool with unknown ordering.

## User Impact
Low discoverability leads to missing BOM scaling, format confusion, and wasted time wiring two commands together. Automation and onboarding both suffer because the CLI does not present itself as a unified interface.

## Error Message Evaluation
Not applicable to subcommand discovery; however, absence of guidance means users are more likely to encounter downstream “file not found” errors for multiplier files.

## Default Behavior Evaluation
- Multiplier file name/location is defaulted in code but not surfaced in help for either command.
- Input ordering (sorted) and output directory defaults remain implicit, so combined flows are opaque.

## Naming & Schema Issues
- Separate executables instead of subcommands hides relationships.
- Conflicting short flags (`-f`) across commands break muscle memory.
- Terminology varies between “qty multipliers,” “qty_multipliers,” and “shared bom.”

## Proposed Improvements
- Present `filare-qty` as a documented subcommand or alias (`filare qty`) and cross-reference it in `filare --help`.
- Provide a command map in help output (or a `filare --commands`/`filare help` section) listing available tasks with one-line descriptions.
- Align short flags or document the conflict prominently; consider unique short flags per command family.
- Add a concise workflow note in both helps: “Run `filare-qty` to create/update multipliers, then `filare -u` to apply them.”

## Required Follow-Up (issues/features/rework)
- docs/issues/cli-subcommand-discovery.md
