# Clarify filare help defaults and add examples

uid: ISS-0005
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

- `filare --help` shows `-f, --formats` defaulting to `hpst` but does not expand the letters beside the option; the expansion is only in the epilog and mixes case (`p` vs `P`).
- Output directory default (first input file’s folder) is not stated; users cannot predict where PNG/HTML land.
- Multiplier options (`--use-qty-multipliers`, `--multiplier-file-name`) do not show defaults or when the file is created/read.
- There are no example invocations, so new users must guess how to combine flags.

## User Impact

Persona A/D copy-paste nothing from the help, leading to trial-and-error with formats and output paths; Persona B cannot rely on deterministic defaults for automation; Persona C lacks predictable behavior for CI setups.

## Suggested Next Steps

- Expand `hpst` inline and add a short table of format codes.
- Show default output directory and default multiplier file name in the option text.
- Add a “Common commands” block (basic render, custom output name/dir, with and without multipliers).
- Mention multi-file ordering (sorted) and that `-c/-d` accept multiple inputs merged in order.
