Here is a **strict, concise, prescriptive** rewrite of **`AGENT.COVERAGE.md`**, including all the requirements you added.

Please review and tell me what to adjust.

---

# AGENT.COVERAGE.md

**Role: COVERAGE**

This agent expands **test coverage** and strengthens **regression guarantees**.
It must not implement features, refactors, or stylistic rewrites.

---

## 1. Mission (Strict)

Your only mission:

1. **Increase pytest coverage** of existing Filare code.
2. **Add YAML regression tests** and **unit tests** where coverage is missing.
3. **Identify dead code** and document it.
4. **Create issues** in the internal docs directory when gaps require another agent.

No other modifications are allowed unless required to make a test possible.

---

## 2. Primary Tools

You must use **pytest** and **pytest-cov** exclusively for measurement.

### Coverage commands:

```bash
uv venv
uv sync
uv run pytest --cov=src/filare --cov-report=term-missing
```

To generate HTML coverage:

```bash
uv run pytest --cov=src/filare --cov-report=html
```

Output appears in `htmlcov/index.html`.

---

## 3. Responsibilities (Strict)

### 3.1 Add Missing Tests

* Add YAML regressions under:

  * `tests/rendering/`
  * `tests/bom/`
* Add Python tests under `tests/` when logic cannot be isolated via YAML.
* Prefer **small, surgical** tests that exercise specific branches or error paths.

### 3.2 Dead Code Identification

If you find code that cannot be reached:

1. Add an entry to `docs/code/dead.md` with:

   * File + function/class name
   * Why it is not reachable
   * Whether removal is likely safe (yes/no + 1-sentence justification)

Example entry:

```
## src/filare/render/output.py::OldOutputFormatter
- Never invoked; replaced by NewOutputFormatter in 2024.
- Safe to remove: YES (surrounded by unused import paths).
```

You **must not** delete the code yourself.

### 3.3 Issue Creation

If you find work that belongs to another role:

Create a markdown issue file in:

```
docs/issues/<short-title>.md
```

The file must include:

```
# Title
Short description of the problem.

## Category
(choose one: REWORK, FEATURE, DOCUMENTATION, TOOLS)

## Evidence
Explain where the problem was observed.

## Suggested Next Steps
1–3 actionable recommendations.
```

You **must not** fix these issues yourself.

---

## 4. Restrictions (Very Strict)

The COVERAGE agent may **NOT**:

* Modify CLI behavior
* Modify YAML schema
* Change function signatures
* Introduce new features
* Perform refactors
* Remove or rename code
* Update documentation except:

  * `docs/code/dead.md`
  * `docs/issues/<issue>.md`

Any other changes must be escalated via an issue.

---

## 5. Workflow

### Step 1 — Run coverage

Use:

```bash
uv run pytest --cov=src/filare --cov-report=term-missing
```

Identify the exact uncovered lines and conditions.

### Step 2 — Add tests

* Create minimal YAML files that trigger the missing branch.
* If YAML cannot reach it, write a direct pytest unit test.
* Keep each test **targeted and compact**.
* Do not rewrite or reorganize code.

### Step 3 — Re-run coverage

Verify the new tests exercise the missing lines.

### Step 4 — Document dead code

If any lines appear unreachable after analysis:

* Add an entry in `docs/code/dead.md`.

### Step 5 — Create issues for other roles

If improving coverage is blocked by missing refactors or unclear logic:

* Create `docs/issues/<issue>.md`.

### Step 6 — Prepare MR

Ensure:

* Only test files + optional dead-code docs + issue files were touched.
* Coverage has improved.
* No unintended modifications exist.

---

## 6. Definition of Done

A COVERAGE task is complete when:

* [ ] Coverage for the targeted module or branch has increased.
* [ ] Tests are minimal, deterministic, and isolated.
* [ ] All unreachable code has been noted in `docs/code/dead.md`.
* [ ] All beyond-scope findings are filed in `docs/issues/*.md`.
* [ ] No feature, refactor, or doc changes were performed.
