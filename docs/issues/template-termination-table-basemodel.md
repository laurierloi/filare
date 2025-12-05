# Add BaseModel for termination_table rows

## Category

UI

## Evidence

- `src/filare/templates/termination_table.html` iterates `rows` with `.source`, `.target`, `.source_termination`, `.target_termination` but no BaseModel/schema defines this shape.
- Missing or misspelled fields surface only as template errors due to StrictUndefined, with no pre-validation.

## User Impact

Contributors and users get runtime failures instead of schema feedback; automation cannot verify inputs before rendering termination tables.

## Suggested Next Steps

- Define a Pydantic BaseModel (e.g., `TerminationRow`) capturing the required fields and types.
- Build the `rows` collection from these models before rendering; document expected shape in template docs and tests.
