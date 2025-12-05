# Make number/unit validation errors actionable

## Category
REWORK

## Evidence
- `src/filare/models/numbers.py:25-41` raises `Exception(f\"{inp} is not a valid number and unit...\")` without indicating the YAML field/key being parsed. Users only see the raw value, not where it came from.
- `src/filare/models/numbers.py:44-55` raises `ValueError(f\"Cannot add {self} and {other}, units not matching\")` but omits the field name and suggests no fix (e.g., which side needs a unit change).

## Suggested Next Steps
1. Include the field/key/context in the error (e.g., `invalid length 'abc' on cable W1; expected '<number> [unit]'`).
2. Use `ValueError` consistently (avoid bare `Exception`) and format messages as one concise line; example: `ValueError: length '1 ft' and '2 m' cannot be added (units must match)`.
3. Add a minimal YAML regression in `tests/rendering/` that triggers the invalid number path to ensure the new message surfaces the field name and designator.
