# Issue/Feature Header Template

Use this header at the top of every file in `docs/issues/` and `docs/features/` to keep planning metadata consistent and to provide stable references for Taskwarrior/Mermaid/Graphviz exports.

```
uid: <immutable-id>          # Format: ISS-<4 digits> for issues (e.g., ISS-0012); FEAT-<AREA>-<4 digits> for features (e.g., FEAT-CLI-0003, FEAT-GRAPH-0010). Immutable after creation.
status: BACKLOG|IN_PROGRESS|BLOCKED|DONE
priority: low|medium|high|urgent
owner_role: FEATURE|REWORK|TOOLS|DOCUMENTATION|COVERAGE|UI|EXPLORATOR|VALIDATOR|JUDGE
estimate: <duration>         # e.g., 2d, 1w
dependencies: [<uid>, ...]  # immutable IDs of blocking items
risk: low|medium|high
milestone: <label>           # e.g., Q1-2025, beta-1.5
```

Guidelines:

- `uid` is the primary key reused across manifest, Taskwarrior, Mermaid, and timelines; keep it short and unique.
- Place the header immediately after the title (or at the top) and keep it in YAML-style key/value lines.
- If an item spans multiple files, pick one canonical `uid` and reference it from related documents.
- Avoid renaming `uid`; if a mistake occurs, add an alias list in the manifest rather than mutating the identifier.
- Suggested area codes for FEAT UIDs: CLI, RENDER, GRAPH, BOM, MECH, DOCS, TOOLS, PERF, UI. Use GENERAL if unsure.
