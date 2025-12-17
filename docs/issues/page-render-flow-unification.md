uid: ISS-0216
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: 3d
dependencies: []
risk: medium
milestone: templates-models

# Unify page rendering via dedicated flow (page/titlepage/din_6771/titleblock)

## Summary

Introduce a dedicated flow for generating HTML pages that all page-like templates use (`page.html`, `titlepage.html`, `din_6771.html`, and their `titleblock`). The flow should:

- Accept the page context (metadata, options, sections like notes/BOM/index).
- Derive required fields (part numbers, sheet info, etc.).
- Build the appropriate TemplateModel(s) (including titleblock).
- Render the HTML via the shared flow so all page renders follow the same path.

This separates “item generation” (BOM, cut, termination, etc.) from page assembly, keeping page rendering consistent.

## Scope / Templates

- page.html and PageTemplateModel
- titlepage.html and TitlePageTemplateModel
- din_6771.html and Din6771TemplateModel
- titleblock.html and TitleblockTemplateModel

## Requirements

- Add a page-render flow (e.g., under `src/filare/flows/pages/`) that assembles context, builds models, and renders.
- Route existing page render call sites (including aux pages) through this flow.
- Keep CLI/user-visible behavior unchanged.
- Add tests to cover the unified flow paths.

## Related

- src/filare/render/html.py
- src/filare/models/templates/page_template_model.py
- src/filare/models/templates/titlepage_template_model.py
- src/filare/models/templates/din_6771_template_model.py
- src/filare/models/templates/titleblock_template_model.py
- docs/issues/template-model-render-refactor.md
