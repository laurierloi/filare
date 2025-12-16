# Overlaps on tutorial titlepage (outputs/tutorial/titlepage.html)
uid: ISS-0214
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

- `filare-check-overlap` (via Playwright container) reports 9 errors on `/workspace/outputs/tutorial/titlepage.html`.
- Examples:
  - `Notes:` text overlaps `tutorial08` and `tutorial08.bom` entries (depths ~8.4 and 6.6 px).
  - Note body lines (e.g., `Wire color is a recommendation`, `Label harnesses with text given in diagram`) overlap index entries (`tutorial08.index`) with depths up to ~10 px.
  - BOM rows (e.g., `Wire, 0.25 mm², BK/RD/YE`) overlap signature fields (`Date`, `created`, `2023-03-29`).

## Hypothesis

- The tutorial titlepage shares the same layout constraints as the examples titlepage: long note lines and dense index/BOM rows are vertically colliding with signature/header fields due to insufficient padding/line-height. The issue is layout/padding in the titlepage template rather than data errors.

## Suggested Next Steps

- Add vertical spacing/wrapping for notes and index rows on the titlepage; ensure BOM and signature blocks have dedicated padding.
- Re-run `filare-check-overlap` to confirm tutorial titlepage is clean.
