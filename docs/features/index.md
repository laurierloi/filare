# Features Index

uid: FEAT-DOCS-0004
status: BACKLOG
priority: medium
owner_role: FEATURE
estimate: TBD
dependencies: []
risk: medium
milestone: backlog


This section collects feature design notes, drafts, and specs. Subfolders group topics such as CLI work (`cli/`), graph/model behaviors (`graph/`), mechanical outputs (`mechanical*`), performance tooling, and parts/ingestion pipelines.

Use these pages to understand planned or in-progress capabilities, edge cases under evaluation, and templates for new feature docs. Each file should describe the goal, current behavior, and any gaps or next steps needed before implementation or release.

## Quick links

- Document model: [Document representation](document-representation.md) and [filare model graph base](filare-model-graph-base.md)
- CLI features and tooling: [CLI command overview](cli-document-commands.md) plus detailed specs under `cli/` (e.g., [code command](cli/code_command.md), [Typer migration](cli-typer-migration.md))
- Graph and rendering behavior: [Graph overview](graph/README.md), [termination diagram flow](graph/termination-diagram-from-graph.md), [bundle/parts links](graph/parts-and-components-links.md)
- Mechanical outputs: [Base schema and paths](mechanical/base-schema-and-paths.md), [labels/dimensions](mechanical/labels-and-dimensions.md), [splices/shielding](mechanical/splices-and-shielding.md)
- Parts and ingestion: [Octopart ingestion](parts/octopart-ingestion.md)
- Performance and profiling: [Performance tooling platform](performance-tools/performance-tooling-platform.md) and related tools under `performance-tools/`
