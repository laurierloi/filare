# BOM tables empty in generated HTML/TSV

## Category

BUG

## Evidence

- Running `source scripts/agent-setup.sh >/dev/null && uv run --no-sync python src/filare/tools/build_examples.py --output-dir /tmp/filare-bom-scan` completes but produces empty BOM tables for many harnesses.
- Example: `/tmp/filare-bom-scan/examples/ex10.bom.html` renders only the header row (`<tr>` count = 1) with no items; `/tmp/filare-bom-scan/examples/ex10.tsv` is likewise header-only.
- Quick scan shows 18 `.bom.html` files with a single `<tr>` (header-only), e.g. `examples/ex01.bom.html`, `examples/ex02.bom.html`, `examples/ex03.bom.html`, `examples/ex04.bom.html`, `examples/ex05.bom.html`, `examples/ex06.bom.html`, `examples/ex07.bom.html`, `examples/ex08.bom.html`, `examples/ex09.bom.html`, `examples/ex10.bom.html`, `examples/ex11.bom.html`, and several tutorial BOMs.

## Hypotheses

- `BomContent.filter_entries` drops any entry without part numbers; most example connectors/cables omit part numbers, so every BOM entry is filtered out before rendering.
- HTML/TSV rendering paths use `BomRenderOptions(filter_entries=True)` by default (e.g., in `Harness.output` and titlepage rendering), so the aggressive filtering is always active.
- The CLI happily succeeds even when BOM tables are empty, so the issue can slip through unnoticed until someone inspects the HTML.

## Plan

- Add a build-time sanity check in `build_examples.py` that fails when a generated HTML contains a `<div id="bom">` with no data rows (header-only), so the problem is caught early.
- Relax BOM filtering so entries without part numbers are still rendered (only drop zero-quantity rows), ensuring example BOMs populate even when P/N fields are absent.
- Rebuild examples/tutorials/demos and verify BOM tables and TSVs now contain rows; keep the new sanity check passing.

## Status

- Resolved locally: BOM filtering now keeps entries without part numbers, and `build_examples.py` fails fast if any BOM HTML renders header-only. Examples/tutorials/demos rebuilt successfully with populated BOM tables.
