# Puppeteer-based doc/diagram preview

## Category

TOOLS

## Evidence

- `docs/tasks.md` includes `230328GTW1_try_to_use_pupeteer` (legacy tooling task) without a tracker.
- No dedicated feature/issue documents current state of browser-based preview/automation for docs or diagrams.

## Expected Outcome

- Decision and implementation note on whether Puppeteer (or alternative) is used for previewing/rendering docs/diagrams.
- If adopted, a minimal script/workflow documented; if rejected, rationale recorded.

## Proposed Next Steps

1. Assess current preview flows (mkdocs serve, static builds) and whether Puppeteer adds value.
2. If useful, prototype a small Puppeteer script to snapshot diagrams/pages; document usage and dependencies.
3. If not needed, close this task with rationale and remove the legacy entry from `docs/tasks.md`.

## Related Items

- `docs/tasks.md` tooling tasks.
