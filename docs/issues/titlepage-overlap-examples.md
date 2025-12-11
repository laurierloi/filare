# Overlaps on examples titlepage (outputs/examples/titlepage.html)

## Category

BUG

## Evidence

- `docker run --rm -v "$PWD:/workspace" filare-overlap "outputs/**/*.html" --viewport 1280x720 --warn-threshold 1 --error-threshold 2 --json outputs/overlap-report.json` reports 26 errors on `/workspace/outputs/examples/titlepage.html`.
- Sample errors (depth in px):
  - `BOM` overlaps `INDEX TABLE` (depth ~17) near the title block headers.
  - Long note text (`Cover all cables with 1/2" or 1/8" black sleeving ...`) overlaps multiple signature fields (`Harness`, `Date`, `Name`, `created` labels).
  - `Designators` overlaps `Content` in the index table header (depth ~11).
  - Various index entries (e.g., `ex10.termination.html`) overlap `Rev`/changelog fields and signature blocks.

## Hypothesis

- The shared examples titlepage packs signature fields, index table headers, and long notes into the same vertical region without enough spacing or line wrapping. Long notes bleed into the signature row; the BOM/INDEX headers collide because they sit on the same line with minimal padding. The template likely needs additional vertical spacing/padding and/or truncation/wrapping for long note strings on the titlepage layout.

## Suggested Next Steps

- Increase vertical spacing between the notes area and the signature row; wrap or clamp long note text on the titlepage.
- Add margin/padding between BOM/INDEX headers in the titlepage grid to avoid header collisions.
- Re-run `filare-check-overlap` after template tweaks to confirm zero errors on `outputs/examples/titlepage.html`.
