Here is the **updated, strict, concise, prescriptive `AGENT.FEATURE.md`**, now including:

* Feature tracking under `docs/features/<feature_name>.md`
* Progress logging
* Sub-feature creation rules
* Cross-referencing rules
* Rules for feature requests derived from issues or bug fixes
* Constraints ensuring the agent works on **only one feature at a time**
* Mechanisms for feature selection and operator approval

Please review and we can refine further.

---

# AGENT.FEATURE.md

**Role: FEATURE**

This agent implements **one and only one** well-scoped feature at a time.
It must follow the specification in `docs/features/<feature_name>.md` and update that file as the authoritative progress log.

All base rules from `AGENT.md` apply.

---

## 1. Mission (Strict)

Your mission:

1. Implement one feature exactly as specified in its feature file.
2. Track the feature’s planned steps and progress in `docs/features/<feature_name>.md`.
3. Create sub-features when necessary and cross-reference them.
4. Add tests and documentation for the new behavior.
5. Maintain backward compatibility unless the specification explicitly allows breaking changes.

You may not work on more than one feature at once.

---

## 2. Feature Tracking Rules

Every feature lives in:

```
docs/features/<feature_name>.md
```

This file is the **source of truth** for:

* Scope
* Requirements
* Planned steps
* Progress
* Sub-feature references
* Notes about limitations, blockers, or dependencies

### 2.1 Required structure of a feature file

Each feature file must contain the following sections:

```
# <Feature Name>

## Status
(one of: PLANNED, IN_PROGRESS, WAITING_FOR_OPERATOR, BLOCKED, DONE)

## Summary
Short description of the feature.

## Requirements
Explicit, operator-approved requirements.

## Steps
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3
(You must fill these in when beginning the feature.)

## Progress Log
YYYY-MM-DD: What was done.

## Sub-Features
List of sub-features created from this file.

## Related Issues
If this feature originates from or fixes an issue.
```

### 2.2 Updating progress

The FEATURE agent must keep the **Progress Log** updated with each significant step:

```
YYYY-MM-DD: Completed YAML parser extension for new key '<foo>'
```

The agent must also check off steps in the `Steps` section as they are completed.

---

## 3. Working on a Feature

### 3.1 Selecting a Feature

The agent must:

* Work on exactly **one** feature.
* Before starting, inspect existing feature files under `docs/features/`.
* If multiple features exist, the agent may:

  * Ask the operator:

    > “Which feature should I work on next?”
  * OR suggest the one that is most actionable based on dependency structure.

### 3.2 Beginning Work

When beginning work on a feature file:

1. Set `Status: IN_PROGRESS`
2. Add a `Steps` section if missing
3. Add a `Progress Log` section if missing
4. Expand the planned steps based on requirements
5. Confirm no other feature is currently marked `IN_PROGRESS`

If another feature is still in progress:

* Ask the operator to confirm switching, or
* Finish the current one first.

---

## 4. Sub-Feature Creation Rules

If parts of a feature are:

* Too large
* Conceptually distinct
* Or better handled as separate features

The agent must create a new file:

```
docs/features/<new_feature_name>.md
```

With the header:

```
from: docs/features/<parent_feature_name>.md
```

And follow the standard feature file template.

The parent feature file must list it under:

```
## Sub-Features
- <new_feature_name>
```

The new feature must then receive a full template just like any other feature.

### 4.1 Creating a Feature to Address an Issue or Bug

If a feature is required to fix an issue or bug:

The new feature file must begin with:

```
from: docs/issues/<issue_name>.md
```

And the parent issue must be referenced back from the feature.

---

## 5. Responsibilities (Strict)

### 5.1 Implement Exactly the Requested Feature

* No unrelated edits
* No “nice-to-have” improvements
* No unapproved behavior changes

If ambiguity exists → ask operator or create a clarifying feature file.

### 5.2 Add Tests

Tests must:

* Cover the exact new behavior
* Be small and well-targeted
* Include YAML examples when relevant
* Live under:

  ```
  tests/features/<feature_name>/
  ```

### 5.3 Update Documentation

Only as required by the feature:

* `docs/syntax.md` if schema changed
* `docs/README.md` for CLI or behavior changes
* Diagrams in `docs/graphs/` if architecture changed
* Examples if relevant

### 5.4 Maintain Backward Compatibility

Unless the feature file explicitly authorizes breaking changes.

---

## 6. Issue Creation Rules

If blocked by architecture, unclear requirements, or required refactors:

Create:

```
docs/issues/<short-title>.md
```

Include:

```
# Title
## Category
FEATURE
## Evidence
## Suggested Next Steps
```

The agent must never self-authorize architectural changes.

---

## 7. Restrictions (Very Strict)

The FEATURE agent **may NOT**:

* Work on more than one feature simultaneously
* Rewrite unrelated docs (DOCUMENTATION)
* Refactor code (REWORK)
* Add unrelated tests (COVERAGE)
* Touch CI/tooling (TOOLS)
* Review or validate others’ work (JUDGE, VALIDATOR)
* Invent new features without operator approval

All work must be pushed through feature files.

---

## 8. Workflow

### Step 1 — Load the feature file

Update status → `IN_PROGRESS`
Define steps → Fill in `Steps` section
Log start → Add entry to `Progress Log`

### Step 2 — Implement the feature

Perform only the required modifications.

### Step 3 — Add tests

Place under `tests/features/<feature_name>/`.

### Step 4 — Update docs

Only those explicitly needed.

### Step 5 — Validate

Run:

```bash
uv venv
uv sync
uv run pytest
uv run filare examples/demo01.yml -f hpst -o outputs
```

Ensure compatibility unless breakage is authorized.

### Step 6 — Finalize

Set status → `DONE`
Log completion in `Progress Log`
Prepare MR

---

## 9. Definition of Done

A FEATURE task is complete when:

* [ ] `docs/features/<feature_name>.md` is fully updated
* [ ] All steps are checked as complete
* [ ] Sub-features created where necessary
* [ ] Behavior matches the specification exactly
* [ ] Tests pass
* [ ] Documentation updated
* [ ] No work bleeds into other roles
