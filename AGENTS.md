# AGENT.md — Base Instructions for All Agents

This document defines **shared rules and workflows** for all agents working on the Filare repository (and its immediate downstream harness repos). Each specialized agent (Refactor, Docs, Tests, etc.) will have its **own extension file**, but must always follow this base guide.

## 1. Goal & Scope

- Your primary goal is to **improve and extend Filare** while keeping:
  - The **CLI stable** (`filare`, `filare-qty`).
  - The **YAML schema backward compatible** unless explicitly told otherwise.
  - The **rendered outputs correct** (Graphviz/HTML/BOM).
- You must:
  - Work in **small, focused branches**.
  - Follow **existing style and architecture**.
  - Keep changes **well-tested** and **well-documented**.

## 2. Repository Layout (What You Can Rely On)

You can assume:

- **Core library & CLI**
  - `src/filare/` — main library code.
  - `src/filare/cli.py` — entrypoint for `filare` and `filare-qty`.
  - Rendering & outputs:
    - `src/filare/render/graphviz.py`
    - `src/filare/render/html.py`
    - `src/filare/render/output.py`
  - Helpers and utilities under `src/filare/tools/`.

- **Documentation & examples**
  - `docs/` — user & dev docs.
  - `docs/graphs/` — Mermaid sources + rendered diagrams.
  - `docs/features/` - Tracking of in-progress or future features
  - `docs/issues/` - Tracking of current issues with the code
  - `docs/bugs/` - Tracking of bugs which have been identified in the codebase
  - `docs/ui/` - Evaluating the UI and serving as a source for improvements
  - `tutorial/` — walkthroughs.
  - `examples/` — ready-made YAML inputs.

- **Tests & regression data**
  - `tests/rendering/`
  - `tests/bom/`
  - Generated outputs belong in `outputs/` or temp directories.

- **Downstream harnesses**
  - `../xsc-harnesses` — used for downstream validation.

## 3. Environment & Commands (Always Use `uv`)

Never call `pip`, `python -m venv`, or raw `python/pytest`. Always use `uv`.

Always use uv for Python commands in this project (virtualenv, installs, running tools).

Never write to or rely on the user’s global cache (e.g. /home/<user>/.cache/uv).

### UV Cache Handling (MANDATORY)

The UV cache directory is **preconfigured** by `source scripts/agent-setup.sh`.

You MUST NOT:

- Set `UV_CACHE_DIR`
- Override `UV_CACHE_DIR`
- Prefix commands with any custom cache path
- Write to `$HOME/.cache/uv`

You MUST rely entirely on the cache configured by.

```bash
source scripts/agent-setup.sh
```

All `uv run` commands automatically use this configured cache.

Do not use sudo and do not try to fix permissions in $HOME (e.g. /home/<user>/.cache/uv). If you hit a
permission error there, stop and report it.

The environment is assumed to be already bootstrapped (`.venv` created and synced).
As an agent, you MUST NOT run `uv venv` or `uv sync`.

### Add packages

```bash
source scripts/agent-setup.sh >/dev/null && uv add <package>
```

### Add dev package

source scripts/agent-setup.sh >/dev/null && uv add --group dev <package>

### Run commands

```bash
source scripts/agent-setup.sh >/dev/null && uv run filare <file>
source scripts/agent-setup.sh >/dev/null && uv run pytest
```

### Build examples

```bash
source scripts/agent-setup.sh >/dev/null && uv run python src/filare/tools/build_examples.py
```

### Restricted Commands

You MUST NEVER:

- Call `uv pip install`
- Call `uv venv`
- Call `uv sync`
- Call `uv sync --group dev` or `--all-groups`

## 4. Coding Style & Conventions

- Python 3.9+
- 4-space indentation
- Black + isort via pre-commit
- Google-style docstrings
- Lowercase module/function names
- Update docs when behaviors change

## 5. Branching, Commits, Merge Requests

### Branch naming

```
<agent_role>/<feature-name>
```

### Commit guidelines

- Small, focused commits
- Imperative commit messages
- Add description when required
- Use conventional commits

#### Short summary of conventional commits

The Conventional Commits specification is a lightweight convention on top of commit messages. It provides an easy set of rules for creating an explicit commit history; which makes it easier to write automated tools on top of. This convention dovetails with SemVer, by describing the features, fixes, and breaking changes made in commit messages.

The commit message should be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

##### Specification:

- Commits MUST be prefixed with a type, which consists of a noun, feat, fix, etc., followed by the OPTIONAL scope, OPTIONAL !, and REQUIRED terminal colon and space.
- The type feat MUST be used when a commit adds a new feature to your application or library.
- The type fix MUST be used when a commit represents a bug fix for your application.
- A scope MAY be provided after a type. A scope MUST consist of a noun describing a section of the codebase surrounded by parenthesis, e.g., fix(parser):
- A description MUST immediately follow the colon and space after the type/scope prefix. The description is a short summary of the code changes, e.g., fix: array parsing issue when multiple spaces were contained in string.
- A longer commit body MAY be provided after the short description, providing additional contextual information about the code changes. The body MUST begin one blank line after the description.
- A commit body is free-form and MAY consist of any number of newline separated paragraphs.
- One or more footers MAY be provided one blank line after the body. Each footer MUST consist of a word token, followed by either a :<space> or <space># separator, followed by a string value (this is inspired by the git trailer convention).
- A footer’s token MUST use - in place of whitespace characters, e.g., Acked-by (this helps differentiate the footer section from a multi-paragraph body). An exception is made for BREAKING CHANGE, which MAY also be used as a token.
- A footer’s value MAY contain spaces and newlines, and parsing MUST terminate when the next valid footer token/separator pair is observed.
- Breaking changes MUST be indicated in the type/scope prefix of a commit, or as an entry in the footer.
- If included as a footer, a breaking change MUST consist of the uppercase text BREAKING CHANGE, followed by a colon, space, and description, e.g., BREAKING CHANGE: environment variables now take precedence over config files.
- If included in the type/scope prefix, breaking changes MUST be indicated by a ! immediately before the :. If ! is used, BREAKING CHANGE: MAY be omitted from the footer section, and the commit description SHALL be used to describe the breaking change.
- Types other than feat and fix MAY be used in your commit messages, e.g., docs: update ref docs.
- example of other types: build:, chore:, ci:, docs:, style:, refactor:, perf:, test:
- The units of information that make up Conventional Commits MUST NOT be treated as case sensitive by implementors, with the exception of BREAKING CHANGE which MUST be uppercase.
- BREAKING-CHANGE MUST be synonymous with BREAKING CHANGE, when used as a token in a footer.

### Repository

- Remote lives on github
- url is https://github.com/laurierloi/filare
- page is https://laurierloi.github.io/filare/
  - it is deployed from the gh-pages branch of the repo
- pypi package is found at: https://pypi.org/project/filare/

# Repository Guidelines

## Project Structure & Module Organization

- Core library and CLI live in `src/filare/`; `cli.py` exposes `filare`/`filare-qty`, with rendering and BOM logic in `render/graphviz.py`, `render/html.py`, `render/output.py`, and helpers under `tools/`.
- Documentation is under `docs/` (see `docs/README.md` and `docs/syntax.md`), with walkthroughs in `tutorial/` and ready-made YAML inputs in `examples/`.
- Architecture/data-flow/model diagrams live in `docs/graphs/`; update the Mermaid sources and regenerate rendered outputs when code structure changes.
- Regression YAMLs live in `tests/rendering/` and `tests/bom/`; write generated outputs to `outputs/` or a temp directory.
- Harness definitions for XSC live next door in `../xsc-harnesses`; treat them as downstream consumers built with the same Filare venv.

## Build, Test, and Development Commands

- Always use the uv package manager for Python (env, installs, and command execution):
  - First-time bootstrap (or when deps change): `uv venv; uv sync`
  - Create venv: `uv venv` # Create venv before running any other command
  - Add a package: `uv add <package>`
  - Install all packages `uv venv; uv sync`
  - Run a Python entrypoint or script: `uv run <command>`
  - Run tests/coverage: `uv run pytest`
  - Avoid `pip`, `python -m venv`, or direct `python`/`pytest` calls; route everything through `uv venv`/`uv run`.
- Quick sanity run: `source scripts/agent-setup.sh >/dev/null && uv run filare examples/demo01.yml -f hpst -o outputs` (HTML/PNG/SVG/TSV). Add `-c examples/components.yml` or `-d metadata.yml` as needed.
- For manual BOM scaling checks: `source scripts/agent-setup.sh >/dev/null && uv run filare-qty tests/bom/bomqty.yml --use-qty-multipliers`.
- Before committing, generate all examples/tutorials via the script used in CI: `source scripts/agent-setup.sh >/dev/null && uv run --no-sync python src/filare/tools/build_examples.py` (then stage the regenerated outputs if needed).
- When you change tests, rerun the relevant pytest suite before committing to keep coverage green.
- Keep `RefactorPlan.txt` up to date: cross out tasks when fully done, add follow-up tasks when work is partial, and record any new features/requests the operator suggests.
- When doing a series of change, track them in <change_name>.temp and keep that file updated as you
  progress

## Coding Style & Naming Conventions

- Python 3.9+; 4-space indentation; follow existing naming (modules, lowercase functions).
- Docstrings follow Google style; keep CLI help strings succinct and user-facing.
- Template and asset names stay lowercase with hyphens or underscores; keep YAML keys lowercase.
- Keep docs coherent with code: when modifying metadata, flows, parser, or render behavior, update `docs/`, `docs/dev/`, and `docs/graphs/` accordingly (metadata guides, syntax, diagrams).

## Testing Guidelines

- No full automated test harness is wired up; use YAMLs in `tests/` and `examples/` to spot rendering/BOM regressions.
- Add a minimal YAML in `tests/rendering/` or `tests/bom/` for new behavior; keep file names numeric-prefixed (`04_newfeature.yml`).
- Also build the XSC harness suite with the project venv (`cd ../xsc-harnesses && WIREVIZ=../Filare-codex1/venv-filare/bin/filare make`) to catch downstream breakage.
- Ensure GraphViz (`dot -V`) and required fonts are available before debugging rendering differences.

Here is the **short, imperative, agent-style version** to paste directly into **AGENTS.md**:

## Non-Interactive Git Rules (MANDATORY)

You MUST run:

```bash
source scripts/agent-setup.sh
```

before executing any Git or GitHub commands.

The env file <.env> MUST exist and SHOULD define GH_TOKEN for GitHub CLI auth.

If `source scripts/agent-setup.sh` fails, you MUST NOT proceed with any Git or GitHub operations.

This enforces a non-interactive, editorless Git configuration.

### Required Behavior

- You MUST provide commit messages explicitly:

  ```bash
  source scripts/agent-setup.sh >/dev/null && git commit -m "<message>"
  ```

- You MUST merge without opening an editor:

  ```bash
  source scripts/agent-setup.sh >/dev/null && git merge <branch> --no-edit
  ```

- You MUST NOT use interactive rebases (`-i`).
  Use:

  ```bash
  source scripts/agent-setup.sh >/dev/null && git rebase <base> --no-edit
  ```

### Forbidden Behavior

- Opening any editor (vim, commit message editor, merge editor, rebase todo).
- Running Git commands that rely on prompts or interactive editing.

If a Git command may open an editor, you MUST rewrite it to a non-interactive form.

## Commit & Pull Request Guidelines

- Open an issue first, then branch from `beta`. Use imperative, concise commit subjects and reference the issue number in the body when applicable.
- Base PRs on `beta`; describe the user-visible change, mention new YAML examples/tests (including any XSC harness updates), and link related issues. Update `docs/syntax.md` when altering the YAML schema or outputs.
- Avoid committing generated artifacts (diagrams, PDFs, tutorials) unless required; keep PRs focused and rebased for a clean history.
- When executing a multi-step plan, complete and commit each step. If no operator input is needed and steps remain, proceed directly to the next step after each commit.
- PR creation flow (target `beta`):
  - Rebase on `origin/beta`, push your branch (`<role>/<desc>`).
  - Ensure that `source scripts/agent-setup.sh` is sourced in the same command
  - Create PR: `source scripts/agent-setup.sh >/dev/null && gh pr create --base beta --head <branch> --title "<type>: <summary>" --body-file pr_body_<branch>.md.temp`.
  - `main` is only for promotion PRs from `beta` after validation; add the `validated` label for beta→main promotion.

## Branding Notes

- Use the Filare brand in user-facing text, CLI help, docs, and examples; keep legacy `filare` names only where required for compatibility.
- Align naming, colors, and tone with `docs/brand.md`; refresh that file alongside any brand-affecting changes.

### MRs

- Target: `beta`
- Set the GitHub default branch to `beta` so PRs default to the correct target.
- PRs to `main` are only allowed from this repository’s `beta` branch after the validation agent has added the `validated` label.
- Keep MR < 30 commits
- Squash on merge
- Avoid committing generated files unless required

## 6. Testing & Validation

- Run tests with:

```bash
uv run pytest
```

- Add YAMLs to `tests/rendering/` or `tests/bom/`
- Build examples
- Optional: build downstream harnesses

## 7. Agent Workflow

### Ramp-up

- Always ask the operator for your role if you don't know it
- Your role must be one of:
  - COVERAGE
  - DOCUMENTATION
  - REWORK
  - FEATURE
  - TOOLS
  - EXPLORATOR
  - JUDGE
  - VALIDATOR
  - UI
  - FIXER
- Read this file + your role-specific guide (AGENT.<ROLE>.md)
- Scan relevant code
- Write a short step plan
- Keep the step plan in `outputs/agents/<your_role>/plan-N`
- Update the step plan as you progress in the execution

### Execution

- Implement → test → update docs → checkout branch -> commit
- The branch you checkout should be <your role>/<feature description>
- Do not open a new branch if you are a judge or validator, you should ask for
  which branch to review or validate
- Continue steps until complete
- Open MR into `beta` on github
- Use the github CLI to open the MR
- Read .env to get necessary credentials
- If a credential you need is not in .env, ask the operator with the specific name and the reason

## 8. Collaboration & Quality Gates

1. Worker agents produce branches
2. Judge agents review
3. Tester agents run full checks
4. Approved work moves beyond `beta` into `main`

## 9. Branding & User-Facing Text

- Use **Filare** consistently
- Follow `docs/brand.md`

## 10. Forbidden Actions

Do **not**:

- Introduce breaking schema or CLI changes
- Delete public APIs without migration
- Commit secrets or machine‑specific configs

## 11. Tools

Agents **MUST** use the following CLI tools when performing search, discovery, and structured config manipulation.
Agents **MUST NOT** use their older or less-reliable counterparts.

### `rg` (ripgrep) — _MANDATORY for code search_

- **USE** `rg` for all file/content searches.
- **DO NOT USE** `grep`, `ag`, or `ack`.
- Fast, respects `.gitignore`, supports `--json`, ideal for locating symbols, definitions, and patterns.
- Example:

  ```bash
  rg --line-number --no-heading "pattern" src/
  ```

### `fd` — _MANDATORY for file discovery_

- **USE** `fd` to list or find files.
- **DO NOT USE** `find`.
- Simpler, faster, respects `.gitignore`, consistent output.
- Example:

  ```bash
  fd ".py" src/
  ```

### `jq` — _MANDATORY for JSON parsing_

- **USE** `jq` to read, filter, or transform JSON produced by tools (pytest, ripgrep, linters).
- **DO NOT USE** ad-hoc text parsing or `python -c` for JSON extraction.
- Example:

  ```bash
  jq '.tests[] | .nodeid' report.json
  ```

### `yq` — _MANDATORY for YAML parsing/editing_

- **USE** `yq` for reading and modifying YAML-based configs (CI, compose files, workflows).
- **DO NOT USE** raw regex, manual indentation edits, or line-by-line sed for YAML.
- Example:

  ```bash
  yq '.services.api.image = "app:latest"' -i docker-compose.yml
  ```

### `just` — _MANDATORY for invoking project tasks_

- **USE** `just` for all predefined project workflows (tests, linting, docs).
- **DO NOT USE** manual inline shell command chains when a recipe exists.
- Ensures consistency, discoverability, and reliable execution.
- Example:

  ```bash
  just test
  ```

---

This base file is shared by all agents. Role-specific guides extend this one.
The role-specific guide is found in agents/AGENT.<ROLE>.md
If you do not know your role, always ask the operator

ALWAYS `source scripts/agent-setup.sh >/dev/null && <your command>` when running a command. It ensures the environment is properly setup for the agent command.
