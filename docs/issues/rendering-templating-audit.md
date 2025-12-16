# Rendering split and templating audit
uid: ISS-0210
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: 3d
dependencies: []
risk: medium
milestone: backlog

## Category

REWORK

## Evidence

- Outstanding render/templating work: finish splitting render/output responsibilities (html/pdf/assets) and audit templating vs. code-built strings; add render smoke tests.
- Layout polish needed for overlapping sections (notes covering diagrams, BOM covering changelog) and connector line merge artifacts.
- Templating changes (e.g., connector pin labels) show the need for broader audit and tests.

## Expected Outcome

- Clear separation of rendering modules (html/pdf/assets) with templates covering presentational output and minimal string concatenation in code.
- Smoke tests for template loading and HTML helpers.
- Layout fixes for overlapping sections and connector merge artifacts.

## Proposed Next Steps

1. Inventory templates vs. code-built markup; move inline HTML generation into templates where appropriate.
2. Add render smoke tests to cover template loading and key helpers (html_utils, assets).
3. Address layout edge cases: overlapping sections, connector merge “bubble” artifacts; add regressions.
4. Document the rendering split and template ownership (which module renders what).

## Related Items

- `docs/features/bom_pagination.md` (rendering/layout changes already done).
