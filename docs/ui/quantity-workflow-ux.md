# Quantity Workflow UX (filare + filare-qty)

## Summary

Quantity multipliers live in a separate executable (`filare-qty`) with minimal help and no workflow guidance. Users must guess defaults, file locations, and order of operations. Integrating quantities into the main CLI would reduce confusion and make CI flows more deterministic.

## Usability Score

2/5 (Poor) — the workflow is discoverable only via source or docs; defaults and sequencing are implicit.

## Observations

- `filare --help` does not mention `filare-qty`; users miss the multiplier step entirely (Persona A/D).
- `filare-qty --help` lacks context, examples, or default file name/path; short flag `-f` conflicts with `filare -f`.
- Default multiplier filename (`quantity_multipliers.txt`) is coded but not surfaced; location is implicit (working dir).
- No guidance on when to run `filare-qty` vs `filare -u`; missing success/error expectations and exit codes for CI (Persona C).
- No machine-readable reports of which multipliers were used/missing.

## Pain Points

- Persona A: Doesn’t discover quantity scaling; cannot copy/paste a full flow.
- Persona B: Cannot validate multipliers before render; deterministic paths and ordering are unclear.
- Persona C: Conflicting flags and lack of JSON outputs make automation brittle.
- Persona D: No workflow walkthrough; “shared bom” terminology unexplained.

## User Impact

Missed multiplier application, inconsistent BOM counts, and fragile scripts. Extra time spent locating files and re-running renders to verify scaling.

## Error Message Evaluation

Help output provides no hints about missing multiplier files or validation errors. Users will only see runtime errors after render starts.

## Default Behavior Evaluation

- Default file: `quantity_multipliers.txt` (not shown in help).
- Default location: working directory (implicit).
- Ordering: multipliers must be created before `filare -u` runs; not documented.

## Naming & Schema Issues

- Flag collision (`-f`) across commands; terminology mixes `qty_multipliers`, `qty-multipliers`, “shared bom.”

## Proposed Improvements

- Integrate quantities as `filare harness qty <cmd>` (init/edit/validate/apply/report) with visible defaults and examples.
- Surface default filename/path in help and errors; provide table/JSON reports for CI.
- Add a workflow doc and CLI examples for the full quantity flow.
- Keep `filare-qty` as a shim with deprecation guidance.

## Required Follow-Up (issues/features/rework)

- docs/features/integrated-quantity-management.md
- docs/issues/filare-qty-help-context.md
