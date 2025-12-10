# Explain filare-qty workflow and flag meanings
uid: ISS-0012
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

- `filare-qty --help` lists only two flags and no command summary, so users cannot tell it generates/updates quantity multipliers for shared BOM scaling.
- Short flag `-f` here means “force new multipliers,” conflicting with `filare -f` meaning “formats,” adding cognitive load when switching commands.
- The multiplier file default (`quantity_multipliers.txt`) and its location are unstated, so users do not know what file will be created or consumed.
- No guidance on how to use the resulting multipliers with `filare --use-qty-multipliers` or what to expect interactively.

## User Impact

Persona A/D do not know when to run `filare-qty` or where the file goes; Persona B cannot predict default paths or workflow order; Persona C cannot script around interactive prompts or differing `-f` semantics.

## Suggested Next Steps

- Add a one-line command summary and a short workflow note (“run before filare to create/update quantity_multipliers.txt for shared BOM scaling”).
- Show the default multiplier file name and directory in the option help; clarify whether prompts occur and how to run non-interactively.
- Consider aligning the short flag for “force new” with a non-conflicting letter or document the discrepancy prominently in the help.
