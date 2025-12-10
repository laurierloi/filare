# Make Filare CLI subcommands discoverable and cohesive

uid: ISS-0004
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Category

UI

## Evidence

- `filare --help` never mentions `filare-qty`; users cannot see that quantity prep exists or when to run it.
- There is no `filare qty` subcommand/alias; instead there are two executables, so the relationship between rendering and multiplier prep is hidden.
- Short flag `-f` means formats in `filare` and force in `filare-qty`, breaking cross-command expectations.
- Default multiplier filename/location and workflow order (run `filare-qty` before `filare -u`) are not visible in either help.

## User Impact

Persona A/D miss BOM scaling entirely; Persona B/C cannot script reliably because commands feel unrelated and flags conflict; extra time is spent rediscovering defaults and wiring commands together.

## Suggested Next Steps

- Add a `filare qty` subcommand or at least cross-link `filare-qty` from `filare --help` with a one-line description and default file name.
- Provide a command list section in help describing each command/task and the expected order (quantity prep then render with `-u`).
- Resolve or document the `-f` flag conflict and surface default multiplier filename/output dir in both helps.
