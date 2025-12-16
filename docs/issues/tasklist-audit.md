# Audit legacy task lists (RefactorPlan, TODO, docs/tasks)
uid: ISS-0211
status: BACKLOG
priority: medium
owner_role: DOCUMENTATION
estimate: 2d
dependencies: []
risk: medium
milestone: backlog

## Category

DOCUMENTATION

## Evidence

- `RefactorPlan.txt` still lists major work items (coverage gaps, Pydantic migration, config/graph models, rendering split, release hygiene, layout polish) with no corresponding entries under `docs/features/` or `docs/issues/` beyond `docs/features/bom_pagination.md`.
- `TODO.md` contains release/branding tasks (PyPI metadata, icons/style, publish on tags, GH Pages) with no tracking docs.
- `docs/tasks.md` lists many legacy tasks (pydantic BaseModel migration, pupeteer preview, ruff hook, connection-only view, dual-color wire, light/dark mode, part library, recursive cables, etc.) without links to current feature/issue records. One item (`bom_on_separate_page_by_config`) is covered by `docs/features/bom_pagination.md`.

## Expected State

Each active task in RefactorPlan/TODO/docs/tasks should be represented by a `docs/features/*` or `docs/issues/*` entry (or marked obsolete), with cross-links so the lists don’t drift from the tracked work.

## Findings

- **Covered:** BOM pagination/derivative diagrams already tracked and marked DONE in `docs/features/bom_pagination.md` (covers RefactorPlan step 11 and `bom_on_separate_page_by_config` in `docs/tasks.md`).
- **Not tracked:** Coverage hardening (RefactorPlan 1–2), Pydantic migration (3, 7, 8, 13), config/graph modeling (4), rendering split/templating audit (5), release/publish hygiene (6 + TODO.md items), BOM correctness (9), layout polish (10), document representation follow-ups (12).
- **Legacy task list items without trackers:** pydantic BaseModel migration, puppeteer preview, ruff pre-commit, connection-only view, dual-color wires, light/dark mode, part library and recursive cables, networkx graph representation, etc.

## Suggested Next Steps

1. Create `docs/issues/coverage-hardening.md` to consolidate RefactorPlan steps 1–2 with current coverage data. ✅
2. Create `docs/features/pydantic-migration.md` (covering RefactorPlan 3, 7, 8, 13 and `docs/tasks` pydantic item). ✅
3. Create `docs/features/config-graph-models.md` (RefactorPlan 4 + docs/tasks networkx/config items). ✅
4. Create `docs/issues/rendering-templating-audit.md` (RefactorPlan 5 + layout polish from step 10). ✅
5. Create `docs/issues/release-hygiene.md` to track TODO.md release/branding tasks and RefactorPlan step 6. ✅
6. Create `docs/issues/bom-and-splice-correctness.md` (RefactorPlan 9). ✅
7. Triaging `docs/tasks.md`: add links to the above trackers, mark `bom_on_separate_page_by_config` as covered by `docs/features/bom_pagination.md`, and prune/close obsolete items after operator review. (Partially done: coverage note added.)

## Impact

Without trackers, task lists drift and contributors can’t tell what’s active or already delivered. Aligning lists with issues/features restores a single source of truth for planning and documentation.

## Questions for Operator

- Are any items in `docs/tasks.md` obsolete and safe to drop instead of tracking (e.g., puppeteer preview, light/dark mode, part library work)?
- Should the release/branding tasks in `TODO.md` move into a single release-hygiene issue, or be split (PyPI metadata vs. GH Pages)?
