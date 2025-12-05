# Detected text overlaps (current outputs)

This summarizes text-overlap findings from `uv run --no-sync filare-check-overlap "outputs/**/*.html" --viewport 1280x720 --warn-threshold 1 --error-threshold 2` after running `build_examples.py`.

## Files with errors
- `outputs/examples/titlepage.html`
  - Collisions: long note “Cover all cables with 1/2"…” overlaps metadata table cells and index links; header blocks (BOM/INDEX TABLE/Designators/Content/Date/Name) collide with links and table entries.
  - Likely cause: very long note on a single line plus dense title page table with minimal spacing.
  - Fix ideas: wrap long notes, cap note width or use `word-break: break-word`, add vertical spacing/margins between note and metadata table, widen header cells or add row padding in title page template.
- `outputs/tutorial/titlepage.html`
  - Collisions: “Notes:” heading and tutorial rows overlap table cells; BOM description cells collide with Date/Name headers.
  - Likely cause: compact table + headings stacked with little margin.
  - Fix ideas: increase row height/padding in tutorial title table, add margins before “Notes:” section, or reduce font size for headers on the title page.
- `outputs/demos/titlepage.html`
  - Collisions: same long note as above overlapping Date/Name/created cells and headers.
  - Likely cause: identical title page structure to examples; long note without wrapping.
  - Fix ideas: same as examples title page—wrap note, add spacing, or constrain note column width.
- `outputs/demos/demo01.html`
  - Collisions: long note overlaps Date/Name/reviewed and BOM/Designators headers.
  - Likely cause: note placed near metadata/BOM headers with limited spacing.
  - Fix ideas: add margin above/below notes, allow multi-line wrapping with constrained width, increase header cell padding.
- `outputs/demos/demo02.html`
  - Collisions: “Crimp ferrule” text overlaps “NO BOM by config! WOW!” header; “0.25 mm²” overlaps list note.
  - Likely cause: header row crowded with nearby annotations and BOM text.
  - Fix ideas: add spacing around BOM header block, allow header text wrap, or reduce font size for the special header.

## Notes
- No other generated pages reported overlaps at the configured thresholds.
- Ignore handling is available via `.filare-overlap-ignore.yml` if some collisions are acceptable, but prefer layout fixes first.
