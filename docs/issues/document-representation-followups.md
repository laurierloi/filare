# Document representation: input + split behavior

## Category

FEATURE

## Evidence

- RefactorPlan step 12 calls for:
  - Accepting `*.document.yaml` as an input to drive generation (not just emit), preserving user edits per hash rules.
  - Ensuring split components (BOM/notes/index) are excluded from the combined page when split output is configured.
  - Updating the index table to link to all generated HTML docs (with split awareness).
  - Adding templates for cut/termination diagram pages and integrating into rendering.
- Current docs/features do not track these follow-ups separately from pagination work.

## Expected Outcome

- Users can supply `*.document.yaml` to drive generation with edits preserved per hash guard.
- Combined pages honor split settings (exclude split sections when split output is requested).
- Index table links include all generated HTML docs, including split pages.
- Templates for cut/termination diagram pages are present and wired.

## Proposed Next Steps

1. Verify current behavior for document input loading and hash-guard preservation; add regression if missing.
2. Ensure split components are excluded from combined page when split outputs are requested; add test.
3. Audit index table links for split pages and fix if missing; add test.
4. Confirm cut/termination templates exist and integrate; add regression if gaps.
5. Update docs to describe document-input workflow and split/index behavior.

## Related Items

- RefactorPlan step 12.
- `docs/features/bom_pagination.md` (covers pagination but not document input/loading).
