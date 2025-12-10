# Add BaseModel for cut_table rows
uid: ISS-0025
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

- `src/filare/templates/cut_table.html` expects `rows` with `.wire`, `.partno`, `.color`, `.length` but no defined BaseModel or schema for those rows.
- Context is assembled ad hoc in rendering; StrictUndefined will fail at runtime without guiding contributors on required fields.

## User Impact

Persona A/B/C contributors cannot safely modify or extend the cut table; mistakes surface as runtime template errors instead of schema validation. CI cannot validate inputs before render.

## Suggested Next Steps

- Introduce a Pydantic BaseModel (e.g., `CutTableRow`) with fields `wire`, `partno`, `color`, `length` and use it to build the `rows` collection passed to the template.
- Document the expected shape in template docs and tests.
