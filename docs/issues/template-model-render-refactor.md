uid: ISS-0215
status: DONE
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
- cut_table: model `CutTableTemplateModel`; usages in `cut` factory, `render/html.py` aux pages. ✅ rendered via builder in factories/aux flow.
- cut: model `CutTemplateModel`; usages in `render/html.py` aux pages, cut factory. ✅ aux pages build full template model.
- termination_table: model `TerminationTableTemplateModel`; usages in `termination` factory, `render/html.py` aux pages. ✅ rendered via builder in factories/aux flow.
- termination: model `TerminationTemplateModel`; usages in `render/html.py` aux pages, termination factory. ✅ aux pages build full template model.
- remaining templates (cable/component_table/simple/simple_connector/colors_macro/images/page) to audit for direct render calls and align with the same pattern. ✅ audited; no remaining direct renders.

## Remaining direct render call sites to migrate
- None; all audited call sites now use template models/flows.

## Progress Log

- 2025-12-11: Workplan created; reset workspace to start template-by-template refactor.
- 2025-12-11: Converted DIN 6771/titlepage factories to use notes/bom builders and TemplateModel.render; BomRender now uses `build_bom_model`; HTML flow renders notes through `build_notes_model`.
- 2025-12-11: Index table now built via `build_index_table_model` (HTML flow, IndexTable.render), removing direct template renders.
- 2025-12-11: Cut and termination templates/factories plus harness aux rows now render via `build_cut_table_model`/`build_termination_table_model`.
- 2025-12-11: Page/titleblock flows now build template models (din/titlepage/simple) before render; aux pages and Graphviz connector/cable rendering run through template builders.
- 2025-12-11: Audited remaining templates (cable/component_table/simple/simple_connector/colors_macro/images/page); no direct render calls remain. Issue closed.

## Related

- src/filare/render/html.py
- src/filare/render/graphviz.py
- src/filare/models/templates/\*
