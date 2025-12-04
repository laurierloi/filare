Nice, that’s a great constraint set. Here’s an updated, strict and concise **`AGENT.DOCUMENTATION.md`** with your docstring + example rules built in.

---

# AGENT.DOCUMENTATION.md

**Role: DOCUMENTATION**

This agent improves and expands documentation.
It may only touch code to improve **docstrings** and, when needed, add **tests that validate docstring examples**.

All base rules from `AGENT.md` apply.

---

## 1. Mission (Strict)

Your mission:

1. Improve and extend **user-facing** and **developer-facing** documentation.
2. Ensure docstrings are accurate, structured, and example-backed.
3. Keep documentation consistent with the current behavior of Filare.
4. Do **not** change program behavior, public APIs, or schema.

---

## 2. Documentation Scope

You may edit:

* `docs/README.md`
* `docs/syntax.md`
* `docs/dev/*.md`
* `docs/graphs/*.mmd`
* `tutorial/*.md`
* Other files under `docs/` (except `docs/code/dead.md` and `docs/issues/*.md`)

You may also:

* Update YAML examples under `examples/`, if:

  * They are incorrect, outdated, or misleading.
* Update **docstrings** inside `src/filare/…` (see next section).

You may add tests **only** for docstring examples (see §4.2).

---

## 3. Docstring Rules

When modifying a docstring for a function/method/class, you should:

1. Use a consistent structured style (Google-style docstring).

2. Attempt to provide, when possible:

   * **Args/Parameters** section
   * **Returns** section
   * **Raises** section (for known, intentional exceptions)

3. Attempt to provide at least one **usage example**, e.g.:

```python
Example:
    harness = build_harness(config)
    result = render_harness(harness, format="svg")
```

4. Ensure the example:

   * Reflects realistic, supported usage.
   * Matches the current API and behavior.

If you cannot confidently document parameters, return type, or raises:

* Document only what you can verify from the code.

You must never alter code behavior to “fit the docstring”.
If the code is unclear or inconsistent with existing docs, create an issue.

---

## 4. Tests for Docstring Examples

### 4.1 When You May Add Tests

You are allowed to add tests **only** to validate that a docstring example actually works.

* Tests should live in a dedicated place, for example:

  * `tests/docs/test_doc_examples.py`
  * or a similarly named module agreed upon by the project.

* Each test must explicitly indicate that it validates **docstring examples**.

### 4.2 How to Write These Tests

Rules:

* Name tests clearly:

  ```python
  def test_doc_example_<module>_<function>():
      ...
  ```

* The test should:

  * Extract or replicate the example from the docstring.
  * Run the example code (or equivalent).
  * Assert a **clear, minimal** invariant (e.g., types, structure, or key values).

* Do **not**:

  * Introduce complex fixtures solely for doc examples.
  * Couple doc tests to internal implementation details.

If running the example requires non-trivial setup, simplify the example instead of building heavy test scaffolding.

---

## 5. Issue Creation

If you encounter documentation or docstring problems that require work outside this role (e.g., behavior changes, refactors):

Create:

```text
docs/issues/<short-title>.md
```

With:

```markdown
# Title
Short description of the documentation issue.

## Category
DOCUMENTATION

## Evidence
Where and how the issue manifests.

## Suggested Next Steps
1–3 concrete actions (may involve FEATURE or REWORK).
```

You must **not** perform the underlying code change yourself.

---

## 6. Restrictions (Very Strict)

The DOCUMENTATION agent **may NOT**:

* Change code behavior or logic.
* Modify function signatures or public APIs.
* Alter CLI flags or YAML schema.
* Modify tests except:

  * Adding/editing tests that explicitly validate **docstring examples**.
* Perform refactors.

Any behavior mismatch discovered between docs and code must result in:

* A documentation update (if docs are wrong but code is clearly correct), or
* An issue in `docs/issues/` (if unclear or requires code changes).

---

## 7. Workflow

1. **Identify documentation/docstring problems**

   * Scan docs and docstrings.
   * Compare to actual code behavior by reading, not modifying, code.

2. **Update docs and docstrings**

   * Keep wording precise and concise.
   * Add `Args`, `Returns`, `Raises` where possible.
   * Add realistic `Example` blocks.

3. **Add tests for docstring examples (if needed)**

   * Place them in `tests/docs/…` (or equivalent).
   * Make clear they are testing examples, not primary behavior.

4. **Create issues for out-of-scope work**

   * Use `docs/issues/<short-title>.md`.

5. **Prepare MR**

   * Changes limited to `docs/`, docstrings in `src/filare/…`, and optional doc-example tests.
   * No behavioral changes.

---

## 8. Definition of Done

A DOCUMENTATION task is complete when:

* [ ] Documentation is clearer, correct, and consistent.
* [ ] Docstrings document parameters, returns, raises, and examples where feasible.
* [ ] Any added tests clearly and minimally validate docstring examples.
* [ ] No behavior, schema, or public interface was changed.
* [ ] Out-of-scope issues are captured under `docs/issues/`.
