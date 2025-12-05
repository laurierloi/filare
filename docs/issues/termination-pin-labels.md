# Termination table omits pin details

## Category
BUG

## Evidence
- Termination diagram rows show only connector designators under "Source" and "Target" but drop the specific pin numbers, making the table ambiguous.

## Suggested Next Steps
- Update termination table generation to include both connector and pin identifiers for each endpoint.
- Add a regression sample (multi-page termination) that asserts pin numbers appear in rendered HTML.
- Rebuild multi-page examples and verify links still point to paginated termination pages (including `.a` for the first page when multiple pages exist).
