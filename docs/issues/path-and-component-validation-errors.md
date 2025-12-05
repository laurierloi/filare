# Make path/component validation errors contextual

## Category
REWORK

## Evidence
- `src/filare/models/utils.py:119-125` raises `"{filename} does not exist."` or `"{filename} is not a file."` without showing cwd or the referencing YAML field, making it hard to locate the bad path.
- `src/filare/models/harness.py:323-338` raise generic `Exception` strings for mismatched types in `connections`/templates without quoting the designator or the type mismatch details.
- `src/filare/models/harness_quantity.py:55-63` raises `ValueError` when `quantity_multipliers.txt` JSON is invalid but does not echo the file path or the malformed content that failed.

## Suggested Next Steps
1. Include full resolved path and caller context in path errors, e.g., `image 'docs/img/missing.png' not found (cwd=/app, referenced by connector X1.image)`.
2. Replace generic connection/type errors with value-aware `ValueError` messages: `connections[1] uses template 'W1' as connector but expected connector template; check metadata/templates`.
3. When parsing `quantity_multipliers.txt`, echo the file path and JSON error: `invalid JSON in outputs/quantity_multipliers.txt: Expecting value at line 1 column 5; delete or fix the file to re-prompt`.
4. Add regression tests that provoke each error and assert the improved messaging without altering behavior.
