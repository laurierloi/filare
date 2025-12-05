# Refactor Follow-ups

Tracked opportunities gathered from docs and in-code TODOs. Keep scope internal-only (no behavior changes).

1) Rendering flow cleanups  
   - `src/filare/render/html.py`: introduce a small data container for replacements to avoid ad-hoc dict assembly; add a PageOption to toggle SVG embedding; move template rendering into class-level methods to consolidate logic.
   - `src/filare/render/graphviz.py`: extend connector/cable style support and add multicolor cable handling; make `ranksep` conditional on diagram density.

2) Pydantic migration (tooling task from `docs/tasks.md`)  
   - Migrate remaining dataclasses toward Pydantic BaseModels stepwise, keeping compatibility shims until callers are updated.

3) Output modularity (task queue in `RefactorPlan.txt`)  
   - Finish splitting render/output responsibilities (HTML/PDF/assets) and audit template-vs-code string generation paths for clarity and testability.
