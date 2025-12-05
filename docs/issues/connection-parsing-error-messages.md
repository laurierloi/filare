# Clarify connection parsing errors

## Category
REWORK

## Evidence
- `src/filare/flows/build_harness.py:203` raises `Exception(f\"{inp} - Found more than one separator ({separator})\")` without pointing to the specific connection entry or designator.
- `build_harness.py:215` raises `Exception(f\"{inp} - Found unexpected characters, e.g. more than one separator\")` with no indication of which connection set failed.
- `build_harness.py:237` raises `ValueError(\"No connection count found in connection set\")` without quoting the offending YAML snippet.
- Template checks (`build_harness.py:379`) emit `Exception(f\"{template} is an unknown template/designator\")` but do not list the available templates or the connection index.

## Suggested Next Steps
1. Include connection index and the offending connection entry in errors, e.g., `connections[2]: entry 'X1:1-2-3' has multiple separators '-'`.
2. Replace bare `Exception` with `ValueError` and ensure messages are single-line, actionable strings.
3. For unknown templates, suggest valid options: `Unknown template/designator 'ABC' (known: X1, W1, templates: ['CONN_A', 'CABLE_A'])`.
4. Add a regression test that feeds malformed `connections` into `build_harness_from_files` and asserts the improved message content (do not change parsing behavior).
