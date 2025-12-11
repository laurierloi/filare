uid: ISS-0038

uid: ISS-0020
status: BACKLOG
priority: medium
owner_role: REWORK
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

# Add just command to extract backlog headers

Category: TOOLS

## Summary

Provide a `just` recipe that scans `docs/issues/**` and `docs/features/**`, extracts their header blocks (`uid`, `status`, `priority`, `owner_role`, `estimate`, `dependencies`, `risk`, `milestone`), and writes a consolidated report to `outputs/headers.md` for quick auditing and manifest generation.

## Evidence

- Headers now exist across all backlog items but require a fast, repeatable way to audit and export them for planning pipelines (Mermaid, Taskwarrior, Graphviz).
- Current inventory was produced ad hoc; a reusable command improves consistency and prevents drift.

## Recommended steps

1. Add a `just` target (e.g., `just export-headers`) that runs a script to parse header blocks from `docs/issues/**` and `docs/features/**`.
2. Emit `outputs/headers.md` containing a table or list of all entries with `uid`, title, path, status, owner_role, priority, milestone, and dependencies.
3. Ensure the command can run offline and fails if required fields are missing.
4. Optionally provide a machine-readable export (JSON/YAML) alongside the markdown for downstream tools.

## Risks/notes

- Must avoid overwriting non-generated files; ensure `outputs/headers.md` is the only target.
- Needs basic validation to catch missing or malformed headers before emitting.
