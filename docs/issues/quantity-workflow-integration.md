# Make quantity workflow discoverable and integrated

## Category

UI

## Evidence

- `filare --help` never references quantity multipliers or `filare-qty`; users miss BOM scaling.
- `filare-qty --help` lacks defaults, examples, and workflow order; short flag `-f` conflicts with `filare -f`.
- Default multiplier filename/location are implicit; no validation/reporting commands exist.

## User Impact

Persona A/D skip the quantity step; Persona B/C cannot script reliable flows or verify applied multipliers; wasted reruns and inconsistent BOM counts.

## Suggested Next Steps

- Integrate quantity commands under the main CLI (e.g., `filare harness qty ...`) with visible defaults.
- Provide validate/report subcommands (table/JSON) and examples showing init → validate → apply sequence.
- Keep `filare-qty` as a shim with a deprecation notice pointing to the integrated commands.
