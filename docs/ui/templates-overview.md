# Template Overview & UX Assessment

## Summary

Filare uses HTML/Jinja templates under `src/filare/templates/` (page, titleblock, BOM, notes, cut/termination tables, etc.). Contexts are assembled ad hoc in `render/html.py` with a small `_RenderReplacements` BaseModel, but most partials (cut/termination tables, notes positioning) lack dedicated view models or documented inputs. Styles and measurements are duplicated across templates, making changes error-prone.

## Usability Score

3/5 (Acceptable) — templates render, but the lack of typed contexts, shared style tokens, and per-template docs raises maintenance risk and cognitive load for contributors.

## Observations

- Context typing is uneven: `_RenderReplacements` (Metadata/PageOptions/Notes) exists, but partials like `cut_table.html` and `termination_table.html` expect row objects with specific attributes without a declared BaseModel.
- Layout values (mm sizes, table widths, BOM positions) are hard-coded in multiple templates; no shared CSS variables or tokens.
- Some templates (e.g., `simple.html`, `simple-connector.html`, `din-6771.html`) appear legacy or niche but have no documented usage or context model, making reuse risky.
- Helper macros (e.g., BOM header) sit inside templates rather than a shared macro file, so conventions are duplicated.
- StrictUndefined is enabled, but missing fields yield runtime errors without pointing to the intended shape of the context.

## Pain Points (Personas)

- Persona A/D: Cannot tell which fields to supply to partials like cut/termination tables; no examples per template.
- Persona B: No clear mapping from data models to template context; adjusting dimensions requires editing multiple files.
- Persona C: Hard to automate rendering variations because template inputs aren’t schema’d or documented.

## Template-by-Template Notes

- `page.html` / `titlepage.html`: Driven by `_RenderReplacements` + `PageOptions`/`Metadata` BaseModels; OK but would benefit from documented context and shared style tokens.
- `titleblock.html`: Relies on `metadata` fields (revisions_list, authors_list, logo, etc.) without a dedicated view model; lots of duplicated sizing literals.
- `bom.html`: Uses BomRender object (not a BaseModel) and inline macro; could expose a simple BOM view model for template consumption.
- `notes.html`: Positions blocks with many arithmetic expressions on `options`; no view model to encapsulate calculated positions/widths.
- `cut_table.html` / `termination_table.html`: Expect `rows` with specific attributes; no BaseModel/schema.
- `simple.html` / `simple-connector.html` / `din-6771.html`: Context is implicit (generator/title/diagram/notes); no BaseModel or usage guidance.
- `component_table.html` / `connector.html` / `cable.html` / `additional_components.html` / `images.html`: Driven by component objects (ComponentModel), but template expectations (e.g., image sizing, partnumbers) are undocumented and partially duplicated.
- `colors_macro.html`: Provides macros but is under-used; other templates re-implement style rather than reusing macros.

## Proposed Improvements

- Define per-template view models (Pydantic BaseModel) for partials: cut table rows, termination rows, notes positioning, titleblock context, legacy “simple” templates.
- Centralize shared style tokens (titleblock dimensions, BOM/notes offsets, table row heights) in a macro or CSS variables to avoid drift.
- Move shared macros (BOM header, revision/author rendering) into a macro file to reduce duplication.
- Add per-template usage notes/examples and document required context keys for contributors.
- Consider deprecating or clearly documenting legacy templates (`simple*.html`, `din-6771.html`) with guidance on when to use them.

## Required Follow-Up

- Create BaseModel issues for templates lacking typed contexts (see separate issues).
- Add a short template README or doc page mapping templates to their context models and usage.
