# demo01 HTML overlap in title block
uid: ISS-0206
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Category

BUG

## Evidence

- `filare-check-overlap` reports 2 errors on `/workspace/outputs/demo01.html`:
  - `BOM` overlaps a revision cell (`td.rev` text `a`) with depth ~2.5 px near the title block.
  - `Designators` overlaps `Content` header in the index table (depth ~12 px).

## Hypothesis

- Title block/table headers are packed too tightly; BOM label and revision cell share the same horizontal space, and the index table headers crowd together. Likely template spacing/padding is insufficient for the header row layout on the demo page.

## Suggested Next Steps

- Add padding/column spacing in the title block/index header on the harness HTML template to separate BOM, revision, and content headers.
- Re-run `filare-check-overlap` to confirm `outputs/demo01.html` is clean.
