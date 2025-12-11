# Align error raises with input validation (RESOLVED)

uid: ISS-0013
status: DONE
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

Generic `Exception` raises in the harness-building flow made it hard to distinguish user input errors from other failures. This update standardizes those cases to `ValueError` and adds regression tests for the failure paths.

## Category

REWORK

## Evidence

- `src/filare/flows/build_harness.py` raised bare `Exception` when no output formats/return types were provided, and when connection sets had inconsistent lengths or ambiguous designator separators.
- No tests asserted the expected exception types for these validation failures.

## Resolution

1. Replace the generic raises in `build_harness_from_files` and `_normalize_connection_set` with `ValueError` to signal invalid inputs.
2. Add targeted tests covering missing outputs/returns, mismatched connection counts, and multiple-separator designators to lock in the expected error types.
