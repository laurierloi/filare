uid: FEAT-CLI-0009
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# CLI: Schema Commands

## Summary

Add a `filare schema` command set to manage interface schemas: generate JSON Schema from interface models and validate user YAML against it.

## Goals

- `filare schema generate` writes the JSON Schema for interface models to a user-specified path (or stdout).
- `filare schema validate <file>` checks YAML inputs against the interface schema and reports errors.
- Keep schema generation tied to Pydantic v2 interface models with full `Field` descriptions.
- Provide machine- and human-friendly output (exit codes + readable errors).

## Non-Goals

- No changes to rendering/BOM flows; this is validation/generation only.
- Not implementing interface editing or example generation here (covered by `filare interface` commands).

## Open Questions

- Default output path/versioning for generated schema.
- Whether to bundle schema in releases or generate on demand.
- Flag for strict vs. lenient validation modes.
