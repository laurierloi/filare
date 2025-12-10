# Project Management for Filare Backlog Coordination

## Summary

Explore how to convert the current markdown backlog in `docs/issues` and `docs/features` into actionable plans (timelines, Gantt charts, Taskwarrior task lists) and whether introducing a PROJET_MANAGER agent would increase coordination, prevent conflicts, and maximize parallel work across agents.

## Use Cases for Filare

- Create a single, time-aware backlog from the existing markdown issues/features to sequence releases and de-risk large refactors (e.g., graph model shift vs CLI restructuring).
- Give agents a reservation/assignment view so they can claim tasks, avoid overlap on shared files (CLI, renderers, docs), and see dependencies.
- Provide leadership with a lightweight roadmap (Gantt) that is exportable to reports without adopting heavy external tooling.
- Allow CI/harness maintainers to see when downstream-breaking items (graph model, Typer CLI migration, mechanical schema) land, so they can stage validation.
- Surface quick wins (docs-only, low coupling) to keep velocity high while long-running items proceed in parallel.

## Technical Evaluation

- Features: derive structured metadata (status, priority, owner/agent role, dependencies, target release, risk) from a small YAML/JSON manifest that references existing markdown files; generate:
  - Mermaid/Graphviz Gantt charts per quarter/milestone.
  - Taskwarrior import files for offline CLI task management.
  - A “workplan” markdown (or `outputs/workplan/*.md`) summarizing assignments and critical paths.
- Strengths: no schema/CLI changes; aligns with existing doc-driven planning; scripts can live under `src/filare/tools/` or `docs/tools/`; outputs are pure docs and compatible with restricted environments.
- Weaknesses: requires consistent metadata upkeep; Gantt accuracy depends on estimates; Taskwarrior adoption needs minimal training; risk of drift if the manifest is not authoritative.
- Limitations: current markdown files lack uniform metadata (only some have Category); dependency mapping must be curated manually at first; auto-detecting file-touch conflicts is heuristic.
- Compatibility with Filare: fits documentation-first approach; leverages existing directories and `just`/`uv run` workflows; does not affect YAML schema or renderers.
- Required integrations: a canonical backlog manifest (e.g., `docs/workplan/backlog.yml`), a generator script (`uv run python ...`) that emits Gantt (Mermaid), Taskwarrior JSON, and markdown rollups; optional hook into `just` to refresh artifacts.

## Complexity Score (1–5)

2 — Mostly documentation and light tooling:

- Changes are confined to docs plus a small parser/generator script.
- No core library or schema impact; minimal new abstractions.
- External APIs (Mermaid, Taskwarrior JSON) are stable and simple.

## Maintenance Risk

- External-side reliability: Mermaid Gantt syntax and Taskwarrior import format are stable; low risk of breaking changes.
- Filare-side work: keeping backlog metadata updated is the main cost; requires ownership discipline.
- Ongoing cost: low, assuming weekly refresh by the PROJET_MANAGER agent or a scheduled `just workplan` job.
- Abandonment risk: minimal because the data lives in-repo; outputs can degrade gracefully (old charts) without breaking builds.

## Industry / Business Usage

- Hardware/embedded teams often maintain lightweight roadmaps (Mermaid/Gantt in repos) to coordinate schematic, harness, and manufacturing documentation work.
- Open-source projects with distributed contributors use markdown roadmaps plus issue labels to stage releases; Taskwarrior is common for CLI-driven personal task tracking.
- Automotive/aerospace documentation teams sequence schema changes and doc updates separately to avoid blocking certification packages—mirrors Filare’s need to stage schema, renderer, and doc tasks.

## Who Uses It & Why It Works for Them

- Linux distros (Debian, Fedora) coordinate releases with task queues and Gantt-like freeze timelines—works because contributors see critical paths early.
- Hardware design teams using KiCad/Altium often keep an internal “work package” spreadsheet or markdown roadmap per release—helps parallelize schematic/layout/BOM work without collisions.
- Rust and Kubernetes release leads rely on markdown roadmaps plus automation that turns issues into burndown charts—gives visibility without heavyweight PM suites.

## Feasibility

- Feasible now: requires only docs and a small generator; no network dependencies beyond existing toolchain.
- Even easier after minor REWORK to add consistent metadata headers to existing issue/feature files.

## Required Work

- REWORK tasks:
  - Add a lightweight metadata header to every `docs/issues/*.md` and `docs/features/**/*.md` (status, priority, owner/role, estimate, dependencies, risk, target release).
  - Normalize naming (one slug per item) to avoid duplicate references across directories, and introduce an explicit immutable `uid` for each item that all outputs (Mermaid, Taskwarrior, timelines) reuse for stable references and user-facing anchors.
- FEATURE tasks:
  - Define and codify a PROJET_MANAGER agent role: maintains backlog manifest, resolves conflicts, sequences dependencies, and assigns roles per item.
  - Introduce a reservation/lock convention (e.g., `assigned:` field or `claims/` log) to reduce toe-stepping across agents.
  - Optional: add a `docs/workplan/backlog.yml` (or JSON) as the source of truth mapping to markdown files, with dependency edges and target milestones.
- DOCUMENTATION tasks:
  - Document the planning workflow in `docs/` (how to add metadata, how to generate charts, how agents claim work, how to request sequencing).
  - Provide examples for adding new items and refreshing outputs.
- TOOLS tasks:
  - Build a generator script (could live under `src/filare/tools/` or `docs/tools/`) that parses the backlog manifest and emits:
    - Mermaid Gantt charts grouped by milestone/workstream.
    - Taskwarrior import JSON (one task per backlog item with tags = role, milestone, dependency).
    - A markdown rollup (workplan) with critical path and parallelization suggestions.
  - Add a `just workplan` (or similar) recipe to regenerate outputs; keep outputs under `outputs/workplan/` or `docs/research/exports/`.
  - Optional: simple conflict detector that flags overlapping assignments on the same module paths (e.g., CLI vs renderers) using a maintained mapping.
- COVERAGE tasks:
  - Unit tests for the generator script (parsing metadata, producing valid Mermaid/Taskwarrior JSON).
  - Regression check that every issue/feature slug is represented in the manifest.

## Recommendation

**ADOPT** — Low complexity and low risk. A structured backlog plus a PROJET_MANAGER agent enables parallelism, clearer sequencing of high-risk changes (graph model, CLI Typer migration, mechanical schema), and reduces collisions between agents.

## References

- docs/issues/_, docs/features/_
- Mermaid Gantt syntax: https://mermaid.js.org/syntax/gantt.html
- Taskwarrior data formats: https://taskwarrior.org/docs/
- Graphviz timelines (for optional export): https://graphviz.org/

## Optional Appendix

- Sample backlog manifest entry (YAML):
  ```yaml
  - id: cli-hierarchical-commands
    file: docs/features/cli-hierarchical-commands.md
    status: backlog
    priority: high
    role: FEATURE
    estimate: 3d
    dependencies: [cli-typer-migration]
    milestone: Q1
    risk: medium
  ```
- Sample Taskwarrior export snippet:
  ```json
  [
    {
      "description": "Implement hierarchical CLI (cli-hierarchical-commands)",
      "project": "filare",
      "tags": ["FEATURE", "CLI", "Q1"],
      "depends": "cli-typer-migration",
      "due": "2025-03-31"
    }
  ]
  ```
- Sample Mermaid Gantt idea:
  ```mermaid
  gantt
    dateFormat  YYYY-MM-DD
    section CLI
    Typer migration           :a1, 2025-01-10, 15d
    Hierarchical commands     :a2, after a1, 12d
    section Graph Model
    Graph base                :b1, 2025-01-05, 20d
    Pins/terminations         :b2, after b1, 15d
  ```
