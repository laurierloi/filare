uid: ISS-0215
status: IN_PROGRESS
priority: medium
owner_role: REWORK
estimate: 3d
dependencies: []
risk: medium
milestone: templates-models

# Refactor template rendering to use explicit model flows

## Summary

For each template, replace ad-hoc `get_template(...).render(...)` calls with an explicit flow that:

- Accepts the concrete inputs for that template (metadata/options/payload).
- Computes any derived fields.
- Instantiates the corresponding `TemplateModel`.
- Returns the model (render happens via `model.render()`).

Track and update call sites template by template to ensure consistency.

## Workplan by template

- notes: model `NotesTemplateModel`; usages in `render/html.py`, `din_6771` factory. ✅ rendered via `build_notes_model` in factories and html flow.
- bom: model `BomTemplateModel`; usages in `render/html.py`, `din_6771` factory, `models/bom.py`. ✅ rendered via `build_bom_model` in factories and BomRender.
- index_table: model `IndexTableTemplateModel`; usages in `render/html.py`, `index_table.py`. ✅ rendered via `build_index_table_model` in html flow and IndexTable.render().
- cut_table: model `CutTableTemplateModel`; usages in `cut` factory, `render/html.py` aux pages.
- cut: model `CutTemplateModel`; usages in `render/html.py` aux pages, cut factory.
- termination_table: model `TerminationTableTemplateModel`; usages in `termination` factory, `render/html.py` aux pages.
- termination: model `TerminationTemplateModel`; usages in `render/html.py` aux pages, termination factory.
- remaining templates (cable/component_table/simple/simple_connector/colors_macro/images/din_6771/page) to audit for direct render calls and align with the same pattern.

## Remaining direct render call sites to migrate
- `src/filare/render/html.py`: titleblock/page renders, aux page renders, table renders.
- `src/filare/render/graphviz.py`: template renders for SVG generation.

## Progress Log

- 2025-12-11: Workplan created; reset workspace to start template-by-template refactor.
- 2025-12-11: Converted DIN 6771/titlepage factories to use notes/bom builders and TemplateModel.render; BomRender now uses `build_bom_model`; HTML flow renders notes through `build_notes_model`.
- 2025-12-11: Index table now built via `build_index_table_model` (HTML flow, IndexTable.render), removing direct template renders.
- 2025-12-11: Cut and termination templates/factories plus harness aux rows now render via `build_cut_table_model`/`build_termination_table_model`.

## Related

- src/filare/render/html.py
- src/filare/render/graphviz.py
- src/filare/models/templates/\*
