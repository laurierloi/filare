# Overlap on root titlepage (outputs/titlepage.html)

## Category

BUG

## Evidence

- `filare-check-overlap` flags `/workspace/outputs/titlepage.html` with an error: `BOM` overlaps `INDEX TABLE` (depth ~17 px) in the title block header area.

## Hypothesis

- The shared titlepage template renders BOM and INDEX headers on the same line with tight spacing; without padding/margin, the labels collide. Likely the same layout/padding issue seen on the examples/tutorial titlepages.

## Suggested Next Steps

- Adjust titlepage header layout to separate BOM/INDEX labels (e.g., add horizontal padding or split onto distinct cells/lines).
- Re-run overlap checker to ensure the root titlepage is clean.
