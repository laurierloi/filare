# Migrate Filare CLI to Typer

## Summary
Adopt Typer for the Filare CLI to enable hierarchical subcommands, richer help/auto-completion, and consistent flag handling. The hierarchical command redesign depends on this migration for clean subcommand UX.

## Motivation (Personas)
- Persona A/D: Need clearer help, examples, and auto-completion to discover commands without reading source.
- Persona B: Wants structured, deterministic commands for segmented validation (metadata → harness → document).
- Persona C: Requires predictable parsing and exit codes for CI; Typer’s Click-based foundation offers type safety and better error messages.

## Proposal
- Replace the current Click entrypoints with a Typer-based app that supports nested subcommands (see hierarchical CLI feature).
- Provide shell completion scripts for common shells.
- Improve help output: show defaults inline, examples per subcommand, and consistent option casing/semantics.
- Preserve backward-compatible shims (`filare`, `filare-qty`) that route to the new Typer app, with deprecation messaging.
- Standardize short flags across subcommands to avoid conflicts (e.g., avoid reusing `-f` for unrelated meanings).

## User Impact
- Discoverable command tree with clearer help and examples.
- Consistent behavior and error formatting across all subcommands, improving scripting reliability.
- Easier onboarding via completions and structured help pages.

## Dependencies / Considerations
- Must coordinate with hierarchical CLI redesign (docs/features/cli-hierarchical-commands.md).
- Update docs, workflows, and tutorials to the new command tree and completions.
- Validate downstream harness scripts for compatibility; provide migration guidance.
- Ensure packaging/entrypoints (`filare`, `filare-qty`) point to the Typer app.

## UI Notes
- Generate shell completions and document how to enable them for bash/zsh/fish.
- Ensure help text shows defaults inline and provides examples per subcommand.
- Keep error messages structured (table/JSON) for CI while readable for technicians.
