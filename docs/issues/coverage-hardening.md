# Raise coverage and document dead code

## Category

FIXER

## Evidence

- RefactorPlan steps 1–2 call out coverage gaps: `models/configs.py`, `connector.py`, `dataclasses.py`, `harness.py`, `tools/build_examples.py`, plus lower modules (colors, cable, bom, utils, render/graphviz, parser/yaml_loader).
- Current coverage report still leaves these modules below the 90% target; dead or unreachable branches aren’t cataloged.

## Expected Outcome

- Identify and document any dead/unreachable code paths for removal instead of force-covering.
- Add targeted tests to raise coverage for the listed modules to ≥90%, or explicitly track exclusions with rationale.

## Impact

Low coverage hides regressions in core parsing/rendering paths; untracked dead code increases maintenance burden.

## Proposed Next Steps

1. Generate fresh coverage with `just test-all` and extract per-file gaps for the listed modules.
2. For each uncovered branch, classify as (a) dead/unreachable (document for removal) or (b) missing tests (add focused tests).
3. Add regression tests for edge cases in `parser/yaml_loader`, `render/graphviz`, and model helpers (`colors`, `utils`); keep them minimal and deterministic.
4. Update coverage report notes and, if needed, add documented exclusions for intentional gaps.

## Related Items

- RefactorPlan steps 1–2 (coverage gaps and hardening).
- `docs/tasks.md` legacy coverage items.
