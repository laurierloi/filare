# Handle external tool failures with actionable errors

uid: ISS-0014
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


## Category

REWORK

## Evidence

- `src/filare/render/pdf.py` directly calls `weasyprint.HTML(...).render().write_pdf(...)` without catching `ImportError`, missing file errors, or `weasyprint` runtime failures; users see stack traces with no hint to install system deps (Pango/fonts).
- Graphviz rendering relies on the `graphviz` Python package; when `dot` is missing or not on PATH, `graphviz.backend.ExecutableNotFound` bubbles up with a raw trace. There is no Filare-side message pointing to Graphviz installation requirements.

## Suggested Next Steps

1. Wrap PDF generation in try/except to emit a concise message: `PDF generation failed: WeasyPrint/GTK/Pango not available or input HTML missing (<path>). Install system deps or drop format 'P'.`
2. Detect `ExecutableNotFound` from Graphviz and rethrow a user-facing `RuntimeError` that mentions `dot`/Graphviz needs to be installed and on PATH (with a link to docs/README install section).
3. Add a minimal regression test that mocks missing Graphviz/WeasyPrint to assert the improved error strings (behavior unchanged except clearer messaging).
