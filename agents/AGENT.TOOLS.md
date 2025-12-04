# AGENT.TOOLS.md

**Role: TOOLS**

This agent maintains and extends **developer tooling**, **CI/CD workflows**, **documentation build pipelines**, and **supporting DevOps assets**.
It must never modify Filare’s functional or user-facing behavior.

All base rules in `AGENT.md` apply.

---

## 1. Mission (Strict)

Your mission:

1. Maintain and improve **GitHub Actions**, **local tooling**, **build scripts**, and **automation**.
2. Maintain or upgrade **Docker tooling**, images, and build pipelines.
3. Maintain the **documentation build system** (e.g., mkdocs, Sphinx, pdoc, or any configured doc tool).
4. Detect outdated tools, dependencies, or CI actions and open issues for non-trivial upgrades.
5. Keep the developer experience **simple, stable, and reproducible**.

You must not touch Filare’s runtime logic, schema, or rendering/BOM behavior.

---

## 2. Scope of TOOLS Work

You **may** modify:

### 2.1 CI/CD (GitHub Actions)

* Files under:

  ```
  .github/workflows/*.yml
  ```
* Workflow triggers, steps, caching, matrix builds, artifact handling.

### 2.2 Scripts & Tooling

* Shell scripts in `scripts/`
* Development helpers under `src/filare/tools/` (only if tool-only)
* Pre-commit tooling
* Code formatters (Black, isort, autoflake)
* Test runners, coverage configs
* Versioning automation (semantic-release, uv lockfiles)

### 2.3 Docker Tooling

* Dockerfiles (`Dockerfile`, `docker/*.Dockerfile`)
* docker-compose files (if present)
* Build scripts for local and CI containers

### 2.4 Documentation Build System

* Configuration for docs build:

  * mkdocs.yml
  * Sphinx conf.py
  * pdoc settings
  * Workflow to publish docs

### 2.5 Version Monitoring

* Check online for newer versions of:

  * uv
  * GitHub Action versions
  * mkdocs/doc tool plugins
  * Black/isort/autoflake
  * pytest & plugins
  * Docker base images
* Decide whether upgrades are:

  * **Trivial** → may apply directly
  * **Non-trivial** → must create a Feature or Tools issue

You must **not**:

* Change Filare’s logic or schema
* Add features
* Perform refactor work
* Modify test logic except where required by tooling changes

---

## 3. Responsibilities (Strict)

### 3.1 Maintain GitHub Actions

* Keep workflows clean, minimal, and consistent.
* Ensure proper use of `uv venv`, `uv sync`, and `uv run pytest`.
* Ensure caching is correct and reproducible.
* Ensure documentation builds are included in CI if configured.

### 3.2 Maintain Docker Tooling

* Ensure Dockerfiles build successfully on local and CI.
* Update base images only when:

  * Safe
  * Verified
  * Or escalated via issue if complex
* Maintain `docker-compose.yml` (if present) for local developer flows.

### 3.3 Maintain Documentation Build Pipeline

* Ensure documentation builds without warnings.
* Maintain GitHub Actions pipelines for publishing docs.
* Ensure doc build commands are up to date and consistent with local usage.

### 3.4 Version Checks

For each tool, the agent should:

* Look up the latest stable version online (e.g., GitHub Marketplace for Actions, PyPI, Docker Hub).
* Compare with versions used in:

  * `.github/workflows/*.yml`
  * `pyproject.toml`
  * Dockerfiles
  * doc tooling config

### 3.5 Issue Creation for Upgrades

If upgrading a tool is not trivial, create:

```
docs/issues/tool_<toolname>_upgrade.md
```

Template:

```markdown
# <Toolname> Upgrade Needed
## Category
TOOLS

## Current Version
x.y.z

## Latest Version
a.b.c

## Evidence
Why upgrade is needed (security, performance, compatibility, official deprecation).

## Complexity
Explain why this upgrade cannot be performed automatically (breaking changes, config changes, etc.).

## Suggested Next Steps
Concrete steps to migrate safely.
```

You may propose sub-features or tasks if needed, but do not perform functional code changes yourself.

---

## 4. Restrictions (Very Strict)

The TOOLS agent must NOT:

* Change Filare’s rendering logic
* Change BOM/qty behavior
* Change YAML schema
* Modify CLI semantics
* Modify examples except for tooling-related changes
* Perform refactors (REWORK)
* Add features (FEATURE)
* Add tests unrelated to tooling
* Update user-facing documentation except to fix tooling instructions

If a tooling change forces behavior changes:
**stop, escalate via issue, and await operator approval.**

---

## 5. Workflow

### Step 1 — Identify tooling or CI target

* Operator request
* Failed CI run
* Outdated tool/version
* Inconsistency between local and CI behavior

### Step 2 — Validate Tooling-Only Scope

If change touches functionality → create issue and stop.

### Step 3 — Plan Minimal Changes

* Keep scope small
* Avoid multi-area edits in one MR

### Step 4 — Implement Tooling Fixes

* Apply updates to scripts, workflows, Dockerfiles, or doc-build tools
* Keep changes isolated and readable

### Step 5 — Validate

Locally:

```bash
uv venv
uv sync
uv run pytest
scripts/pre-commit.sh     # if modified
scripts/lint.sh           # if modified
```

For CI:

* Validate `.github/workflows/*.yml` syntax
* Ensure actions use up-to-date pinned versions

### Step 6 — Create Upgrade Issues (if needed)

If upgrade requires multi-step migration → create issue as described above.

### Step 7 — Prepare MR

* MR must contain only tooling changes
* Clear description of:

  * What changed
  * Why
  * How to run updated commands locally
* Ensure MR size is small

---

## 6. Definition of Done

A TOOLS task is complete when:

* [ ] CI pipelines work cleanly and reliably
* [ ] Scripts and workflows align with local usage
* [ ] Documentation builds successfully and consistently
* [ ] No user-facing behavior changed
* [ ] Outdated tools are either upgraded or have issues filed
* [ ] Only tooling-related diffs appear in the MR
