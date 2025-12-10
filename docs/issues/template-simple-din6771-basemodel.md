# Add BaseModel/context schema for legacy simple templates
uid: ISS-0030
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Category

UI

## Evidence

- `src/filare/templates/simple.html`, `simple-connector.html`, and `din-6771.html` rely on implicit context keys (`generator`, `title`, `diagram`, `notes`, etc.) with no documented BaseModel.
- Usage is unclear; no schema validation protects contributors from missing/mistyped keys.

## User Impact

Developers cannot confidently reuse or extend these templates; errors show up only at render time. Personas A/D have no guidance on when or how to use these templates.

## Suggested Next Steps

- Define a small Pydantic view model describing the expected context for these templates (title, generator, diagram HTML/SVG, notes text, optional component info).
- Document intended use cases (e.g., lightweight outputs) and include example data in template docs/tests.
