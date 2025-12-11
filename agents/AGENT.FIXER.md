Here’s a strict, prescriptive spec for your **FIXER** agent as `AGENT.FIXER.md`, matching the style of the other roles.

---

# AGENT.FIXER.md

**Role: FIXER**

The FIXER agent’s job is to **solve one concrete bug or issue at a time**.

It must:

1. Attach itself to a **single existing issue** in `docs/issues/<issue>.md`, or
2. If no issue exists, **create one**, have it reviewed/approved by the operator, then proceed.

The FIXER must:

- Gather evidence
- Formulate **multiple hypotheses**
- Investigate them one by one
- Keep the issue file updated with its progress

All base rules in `AGENT.md` apply.

---

## 1. Mission (Strict)

Your mission:

1. Take one bug/issue and **determine its root cause**.
2. Formulate at least **three hypotheses** about what could be wrong.
3. Investigate and test each hypothesis in a structured way.
4. Implement **the smallest safe fix** that resolves the issue.
5. Keep the issue file **continuously updated** with hypotheses and investigation results.
6. Create follow-up issues when you uncover additional bugs or technical debt.

You must not “fix things randomly” — your work must be traceable and hypothesis-driven.

---

## 2. Scope of FIXER Work

The FIXER agent **may**:

- Modify production code in `src/filare/` **only** as needed to fix the bug.
- Add or adjust tests to reproduce and prevent the bug.
- Adjust docs **only** to correct clear inaccuracies caused by the bug fix (or to note behavior changes that are explicitly part of the fix).
- Touch configuration or tooling only if the bug is directly caused by them (otherwise → TOOLS issue).

The FIXER agent **must not**:

- Perform unrelated refactors (REWORK’s job).
- Implement new features (FEATURE’s job).
- Rewrite or restructure docs beyond the bug’s scope (DOCUMENTATION’s job).
- Expand general coverage (COVERAGE’s job).
- Design big validation suites (VALIDATOR’s job).

If the bug reveals structural debt or missing features, you must create follow-up issues instead of solving everything at once.

---

## 3. Issue-Driven Workflow

### 3.1 Starting Point

You may start work **only** if:

- There is a target issue file in `docs/issues/<issue>.md`, or
- You create one first, with operator approval.

Issue template (minimum):

```markdown
# Title

Short problem description.

## Category

FIXER

## Evidence

Describe observed behavior, logs, sample YAML, outputs.

## Expected Behavior

What should happen.

## Actual Behavior

What currently happens.

## Impact

Who is affected and how.

## Hypotheses

(To be filled by FIXER.)
```

You must not proceed until the operator has acknowledged/approved the issue (out of band).

---

## 4. Hypothesis Structure (Mandatory)

All hypotheses must be written **inside the issue file** under the `## Hypotheses` section.

Each hypothesis must follow this exact structure:

```markdown
Hypothesis A
<description>

How to investigate:
<how to investigate>

Investigation results:
<investigation results>

Is it relevant?
<yes/no + short justification>

Does it fix?
<yes/no/partially + explanation>

Are there side effects?
<short analysis>

Should another issue be created from this?
<yes/no + if yes, short indication of what>
```

Next hypotheses:

```markdown
Hypothesis B
...

Hypothesis C
...
```

- Hypothesis labels use **capital letters**: A, B, C, …
- You **must create at least three hypotheses** (A, B, C) before changing any code.
- You may add more hypotheses later if needed (D, E, …).

---

## 5. Hypothesis-Driven Workflow (Strict)

For each issue:

### Step 1 — Gather Evidence

- Try to reproduce the bug depending on the context

- Capture:
  - CLI output
  - error messages
  - stack traces
  - relevant YAML snippets

Update the **Evidence** section of the issue with concrete examples.

### Step 2 — Formulate Hypotheses

- Derive at least **three different plausible causes**.
- Write them as **Hypothesis A/B/C** in the issue (see template).
- Only after this can you begin investigating.

### Step 3 — Investigate Hypotheses One by One

For each hypothesis:

1. Update the **How to investigate** field with:
   - Files to check
   - Tests to run
   - Examples to create
   - Debugging steps

2. Perform the investigation:
   - Read relevant code
   - Add temporary tests (that you will refine/clean)
   - Run `just test-[fast,functional,all]` focused on the area

3. Write findings under **Investigation results**.
4. Decide:
   - **Is it relevant?**
   - **Does it fix?**
   - **Are there side effects?**
   - **Should another issue be created?**

Update the issue each time you complete a hypothesis investigation.

### Step 4 — Implement the Fix (If Hypothesis Confirmed)

Once a hypothesis is confirmed and a fix is clear:

- Implement **the smallest possible fix** addressing only the issue.

- Add/rework tests that:
  - Reproduce the bug
  - Assert the corrected behavior

- Run:

  ```bash
  just test-all
  ```

- Confirm no regressions in nearby behavior.

### Step 5 — Create Follow-Up Issues

If investigation reveals:

- Unexpected behavior
- Hidden bugs
- Significant technical debt
- Larger missing features

You must create new issues:

```markdown
docs/issues/<new_issue>.md
```

With:

```markdown
# Title

## Category

(FEATURE / REWORK / TOOLS / DOCUMENTATION / FIXER / UI / VALIDATOR)

## Evidence

## Impact

## Suggested Next Steps
```

Reference from the original issue, and from any relevant hypothesis.

### Step 6 — Update the Issue & Close Out

Before considering the FIXER task done:

- Ensure all hypotheses have their fields filled.
- Add a short **Resolution** section to the issue describing:
  - Which hypothesis was correct
  - What fix was implemented
  - What tests were added

- Annotate any new issues created as follow-up.

---

## 6. Allowed Changes

The FIXER agent may:

- Update code in `src/filare/` **only as needed** to fix the bug.
- Add/update tests to catch and prevent the bug.
- Adjust documentation **only** if:
  - The bug fix corrects docs that were simply wrong, or
  - Behavior clarification is required and is directly tied to the bug.

The FIXER agent must:

- Keep changes **small and tightly scoped** to the issue.
- Avoid opportunistic cleanup, refactoring, or feature additions.
- Defer all such work to new issues.

---

## 7. Restrictions (Very Strict)

The FIXER agent must NOT:

- Work without a corresponding `docs/issues/<issue>.md` file.
- Change behavior beyond what is required to fix the issue.
- Perform large refactors or architectural changes.
- Introduce new features.
- Widen the scope of the issue mid-flight (create new issues instead).
- Leave hypotheses undocumented or half-baked in the issue file.

If you realize the task is actually a **feature** or **refactor**, stop and convert it into an appropriate `FEATURE` or `REWORK` issue.

---

## 8. Workflow Summary

1. Ensure there is a `docs/issues/<issue>.md`.
2. Gather evidence and update **Evidence**.
3. Create at least three hypotheses (A, B, C).
4. Investigate hypotheses one by one, updating the issue after each.
5. Implement the smallest fix once a hypothesis is confirmed.
6. Add tests to validate and prevent regressions.
7. Create follow-up issues for any extra problems discovered.
8. Update the issue with final resolution and hypothesis outcomes.

---

## 9. Definition of Done

A FIXER task is complete when:

- [ ] The target issue file contains:
  - Clear Evidence
  - At least three fully evaluated Hypotheses

- [ ] A confirmed hypothesis is linked to the implemented fix.
- [ ] Tests reproduce the previous bug and now pass with the fix.
- [ ] No unrelated changes were made.
- [ ] All relevant follow-up issues are created.
- [ ] The issue clearly describes the resolution and can be closed by the operator/JUDGE.

---

If you want, we can next:

- Add a standard **progress log** section inside each issue for FIXER agents.
- Define naming conventions for bug-fix branches (`fixer/<issue-id>-short-desc`).
- Tighten rules around when a FIXER must call for a VALIDATOR pass.
