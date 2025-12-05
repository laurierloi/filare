# Standardize error logging when wrapping exceptions (OPEN)

Exception wrapping now uses typed Filare errors, but logging behavior is inconsistent (some wrappers log before raising, others do not). Define a consistent guideline to avoid duplicate log noise while preserving context.

## Category

REWORK

## Evidence

- `src/filare/flows/build_harness.py` logs metadata errors before wrapping in `FilareFlowException`, while other conversions (e.g., parser/tools/model errors) do not log.
- No documented guideline for when to log-and-raise versus raise-only.

## Next Steps

1. Adopt: only log at top-level call sites where errors are handled; do not log inside helpers that immediately re-raise.
2. Apply consistently across flow/model/parser/render/tool layers.
3. Document the pattern in developer docs and add a lint/checklist entry.
