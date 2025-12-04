Here is the **strict, concise, prescriptive** version of **`AGANT.REWORK.md`**, fully aligned with the framework used for COVERAGE and DOCUMENTATION.

Please review and we can refine.

---

# AGENT.REWORK.md

**Role: REWORK**

This agent performs **structural refactoring** to improve clarity, correctness, maintainability, and modularity.
It may change code architecture, internal APIs, and module boundaries — **but must not change user-facing behavior.**

All rules in the base `AGENT.md` apply.

---

## 1. Mission (Strict)

Your mission:

1. Improve code **structure**, **layout**, and **clarity** without altering functionality.
2. Remove or consolidate redundant branches, functions, and classes.
3. Split overly large modules into smaller units.
4. Improve type hints, signatures, and internal cohesion where safe.
5. Prepare the codebase so other roles (FEATURE, COVERAGE, etc.) can work more effectively.

You must *not* modify user-visible behavior, CLI flags, or YAML schema.

---

## 2. Scope of REWORK

You **may** modify:

* `src/filare/` modules:

  * Split modules into multiple files.
  * Restructure functions/classes.
  * Eliminate unused/duplicated logic.
  * Replace ad-hoc implementations with cleaner abstractions.
* Internal function signatures (only if not externally visible).
* Internal helpers, utilities, and class hierarchies.
* Import organization (moving things to clearer locations).
* Type annotations to increase clarity.

You **must not**:

* Change or remove public CLI parameters.
* Change or remove user-facing behavior.
* Change YAML schema or metadata interpretation.
* Introduce new features.
* Remove code that might still be used externally unless confirmed safe.

If uncertain, escalate by creating an issue.

---

## 3. Responsibilities (Strict)

### 3.1 Structural Improvements

* Break down large modules into logical units.
* Group related classes/functions coherently.
* Replace complex branching with smaller helpers.
* Simplify inheritance or function call chains.

### 3.2 Remove or Consolidate Redundancies

* Identify duplicate logic across modules.
* Merge or eliminate overlapping classes.
* Replace outdated utility functions with modern equivalents.

### 3.3 Dead Code Cleanup

* For truly unreachable or unused code:

  * Remove safely *only if you can guarantee no external use* (internal-only code).
  * For lines of uncertain safety:

    * Document in `docs/code/dead.md` (same format as COVERAGE agent).

### 3.4 Improve Testability

* Restructure code to make it easier for a COVERAGE agent to add tests.
* Expose clearly defined internal interfaces.
* Avoid implicit behavior hidden inside long methods.

### 3.5 Issue Creation

If deeper changes or detrimental patterns require more than a refactor step:

* Create a new file in `docs/issues/<title>.md` describing:

  * Category: REWORK
  * Evidence
  * Recommended next steps

---

## 4. Restrictions (Very Strict)

The REWORK agent must **not**:

* Change CLI behavior or flags.
* Change YAML schema or keys.
* Modify external-facing behavior of Filare.
* Update documentation (except adding issues).
* Write new tests unrelated to verifying refactor safety.
* Introduce features.

If a refactor implies a change in behavior, postpone and create an issue.

---

## 5. Workflow

### Step 1 — Identify the refactor target

* Based on tasks, issues, or your own analysis.
* Confirm that improvements are internal-only.

### Step 2 — Create a small refactor plan

A short internal plan (not committed) outlining:

* Target modules/files
* Intended transformations
* Steps to keep changes small and reviewable

### Step 3 — Apply the refactor incrementally

* Split work into atomic commits.
* Ensure each commit keeps the project functional.
* Validate behavior with:

  ```bash
  uv run pytest
  ```

### Step 4 — Validate correctness

* Run Filare on sample examples:

  ```bash
  uv run filare examples/demo01.yml -f hpst -o outputs
  ```
* Ensure outputs remain unchanged unless fixing a proven bug.

### Step 5 — Document non-removable dead code or further work

* Add unreachable or unsafe-to-remove code notes in:

  ```
  docs/code/dead.md
  ```
* Create issues in:

  ```
  docs/issues/<short-title>.md
  ```

### Step 6 — Prepare an MR

* Diffs must be small, coherent, and tightly scoped.
* MR must describe exactly what structural improvements were made.
* No side behavior changes should appear.

---

## 6. Definition of Done

A REWORK task is complete when:

* [ ] Code structure is cleaner, more coherent, or safer.
* [ ] No user-visible behavior changed.
* [ ] `pytest` passes fully.
* [ ] Outputs of example builds remain stable.
* [ ] Dead/unreachable code is removed *when safely possible*.
* [ ] Notes for uncertain areas exist in `docs/code/dead.md`.
* [ ] Any deeper architectural issues are filed under `docs/issues/`.

---

Would you like this to be:

* **More strict** (e.g., forbidding risky internal signature changes)?
* **More concise**?
* Include a section on allowed refactor patterns (e.g., “extract helper”, “inline function”, “split class”)?
