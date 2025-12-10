# Clarify color and component validation errors
uid: ISS-0005
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Category

REWORK

## Evidence

- `src/filare/models/dataclasses.py:794` raises `Exception("Unknown color code")` with no mention of the input value, designator, or accepted codes.
- `dataclasses.py:806-814` raise generic `Exception` strings when additional component lists mismatch wirecount or are used on bundles, without pointing to the cable ID or the list length mismatch.
- `dataclasses.py:639` raises `ValueError(f"Failed to find a color for property: {self}")` which prints an object repr instead of the specific missing field.

## Suggested Next Steps

1. Replace generic `Exception` with `ValueError` and include designator and offending value, e.g., `cable W1: color code 'PR' is not in ['BK','RD',...]`.
2. For component list length checks, report the expected vs. actual counts and the field name: `cable W1 additional_components lengths (2) must match wirecount 4`.
3. Add a regression test YAML that triggers each path (invalid color code, mismatched additional component list) and asserts the improved message text without changing behavior.
