# CI workflow calls build_examples with invalid group

uid: ISS-0215
status: IN_PROGRESS
priority: high
owner_role: FIXER
estimate: TBD
dependencies: []
risk: medium
milestone: backlog

## Category

BUG

## Evidence

- PR https://github.com/laurierloi/filare/pull/80 fails in CI when invoking `build_examples.py -g examples`.
- Local repro: `source scripts/agent-setup.sh >/dev/null && uv run --no-sync python src/filare/tools/build_examples.py -g examples` exits with `argument -g/--groups: invalid choice: 'examples'` and lists the allowed groups (`basic`, `minimal-document`, `document-cut`, `document-termination`, `multi-page`, `all-document`, `tutorial`).

## Expected Behavior

- CI should call `build_examples.py` with supported groups (or omit `-g`) so example builds complete.

## Actual Behavior

- CI passes `-g examples`, which is not a valid group name, causing argument parsing to fail before any examples are built.

## Impact

- The workflow step fails immediately, blocking PR validation and preventing example outputs from being regenerated.

## Hypotheses

Hypothesis A
The GitHub Actions workflow hardcodes `-g examples`, a legacy/wrong group name.

How to investigate:
- Inspect `.github/workflows` for `build_examples.py -g` usage and confirm arguments.

Investigation results:
- `.github/workflows/ci.yml` calls `uv run python src/filare/tools/build_examples.py --output-dir outputs --group examples` and `--group demos`; `examples` is invalid, and `demos` was not defined in the script until added in this fix.

Is it relevant?
- Yes; the invalid arguments are exactly what argparse rejects in CI.

Does it fix?
- Yes; updated the workflow to call `build_examples.py` with supported groups (basic, minimal-document, document-cut, document-termination, multi-page, all-document) and write to `outputs/examples`, removing the invalid `demos` step.

Are there side effects?
- Low: examples now land under `outputs/examples/<group>` (still under `outputs/`), aligning with the docs sync step.

Should another issue be created from this?
- No.

## Resolution

- Root cause: CI workflow invoked `build_examples.py` with unsupported groups (`examples`, `demos`), causing argparse validation failure.
- Fix: Updated `.github/workflows/ci.yml` to build valid groups (basic, minimal-document, document-cut, document-termination, multi-page, all-document) into `outputs/examples`, with one step per group; kept tutorial build separate and removed the invalid `demos` step.
- Added `demos` as a supported group in `src/filare/tools/build_examples.py` (covers `examples/demo01.yml` and `examples/demo02.yml`) and restored a CI step to build it.
- Status: Workflow commands use only supported group keys; CI should proceed past the example build stage.

Hypothesis B
`Justfile` or local helper scripts feed `-g examples` into CI, so the workflow inherits the invalid argument from a shared recipe.

How to investigate:
- Check `Justfile` and any invoked scripts (`scripts/*.sh`) used by the CI job for build_examples arguments.

Investigation results:
- No `Justfile` is present; no other scripts currently feed `-g examples` into CI. The bad arguments are only in `.github/workflows/ci.yml`.

Is it relevant?
- No direct action needed beyond fixing the workflow.

Does it fix?
- No; confirming the source only.

Are there side effects?
- None.

Should another issue be created from this?
- No.

Hypothesis C
Group definitions in `build_examples.py` changed recently, and CI is still using an outdated group alias (`examples`) that should be mapped or removed.

How to investigate:
- Review `src/filare/tools/build_examples.py` group definitions and git history to see if `examples` used to be valid and whether a compatibility alias is needed.

Investigation results:
- `src/filare/tools/build_examples.py` defines groups: basic, minimal-document, document-cut, document-termination, multi-page, all-document, tutorial. No alias for `examples`/`demos` exists.

Is it relevant?
- Yes; confirms CI must use these keys (or omit `--groups` to run all).

Does it fix?
- No change needed in the script; fix belongs in workflow arguments.

Are there side effects?
- None.

Should another issue be created from this?
- No.
