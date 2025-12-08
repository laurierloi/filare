# Filare CI Pipeline

This repository uses:

- A main CI workflow (`.github/workflows/ci.yml`, named “Filare Main CI (release path)”) that runs on pushes to `main`/`beta` and on pull requests targeting `main` (release/publish path).
- A beta PR CI workflow (`.github/workflows/pr-beta-ci.yml`) that runs on pull requests targeting `beta` (lint → tests only).
- A lightweight guard workflow (`.github/workflows/pr-target-beta.yml`) that enforces the beta-first flow by blocking PRs that bypass `beta` or attempt to merge into `main` without prior validation.

## Branch & validation flow

- Default PR base is `beta`; set the repository’s default branch to `beta` in GitHub settings so the GitHub UI/`gh pr create` offer `beta` by default.
- Beta PRs run `.github/workflows/pr-beta-ci.yml` (lint, then tests).
- A PR targeting `main` is allowed only when the head branch is this repository’s `beta` branch and the PR carries the `validated` label (added by the validation agent); it runs the full `.github/workflows/ci.yml`.
- All other PR targets will fail the `Enforce beta as default base` check and must be retargeted to `beta`.
- Ensure the repository has a `validated` label so the validation agent can tag the `beta` → `main` promotion PR.

## Jobs / Stages

1. **Lint**
   - Runs `black --check` on `src/` and `tests/`.
   - Runs `prettier --check` on docs and templates.
   - Requires Python (3.11) and Node (for prettier).

2. **Tests**
   - Installs graphviz and project + dev deps.
   - Runs unit suite only: `pytest -m unit` (functional/documentation tests are opt-in).
   - Uses the same Python version as lint.

3. **Build examples/templates**
   - Installs graphviz + project.
   - Runs `filare` to generate outputs from examples/tutorials.
   - Uploads `outputs/` as an artifact for later stages.

4. **Text overlap check (pushes only)**
   - Uses Playwright/Chromium (container image) to detect overlapping text across generated HTML outputs.
   - Runs only on pushes (not PRs); uses `filare-check-overlap` with warning/error thresholds and optional ignores.

5. **Docs / gh-pages (main only)**
   - Copies `docs/` into `site/` and includes built example artifacts if present.
   - Publishes `site/` to GitHub Pages via `peaceiris/actions-gh-pages`.

6. **Document representation build (planned)**
   - Build up to `DocumentRepresentation` YAML (with hashes) without rendering final assets, to validate graph/document assembly.
   - Useful for faster CI checks before full render/publish steps.

7. **Release (semantic-release, main only)**
   - Uses `python-semantic-release` to bump the version, update `VERSION`, and publish release assets.
   - Gating: downstream publish/verify/container steps run only if either the `VERSION` file changed or a new tag was created during the run (prevents double-publishing).
   - Generates/updates `CHANGELOG.md` automatically and commits it with the release bump.
   - Needs `GH_TOKEN` (GitHub token) and `PYPI_TOKEN` (if publishing to PyPI through semantic-release).

8. **Publish to PyPI (main only)**
   - Builds the distribution (`python -m build`).
   - Uploads via `twine` using `PYPI_TOKEN`.

9. **Verify PyPI**
   - Installs `filare` from PyPI and checks `filare --help`.

10. **Container (GHCR)**

- Builds a Docker image and pushes to `ghcr.io/${{ github.repository }}:latest`.
- Uses `GITHUB_TOKEN` for registry auth.

## Required Secrets

- `PYPI_TOKEN`: PyPI API token for publishing.
- `GH_TOKEN`: (optional) used by semantic-release for tagging; `GITHUB_TOKEN` provided by Actions is usually sufficient.
- GitHub Pages and GHCR steps use the built-in `GITHUB_TOKEN`.
- Tag-triggered release workflow (`release-on-tag.yml`) relies on `PYPI_TOKEN` and `GITHUB_TOKEN`; ensure `VERSION` matches the tag when releasing manually.

## Local Reproduction

- Lint: `black --check src tests` and `prettier --check "docs/**/*.{md,html}" "src/filare/templates/**/*.html"`.
- Tests: `pytest -m unit` (use `pytest -m "unit or functional" --include-functional` to add slow documentation/functional tests; ensure `graphviz` is installed).
- Examples: `filare -f hs -o outputs/examples examples/demo01.yml`.
- Build dist: `python -m build`.
- Docker: `docker build -t filare-local .`.

## Creating/Updating the Pipeline

1. Edit `.github/workflows/ci.yml` to adjust stages, Python/Node versions, or paths.
2. Ensure secrets (`PYPI_TOKEN`) are set in the repo settings.
3. Push to `beta` or `main` to exercise lint/tests/examples and text-overlap checks; push to `main` to run docs/publish/release. PRs to `beta` run the dedicated beta PR lint/test workflow; PRs to `main` run the full CI.
4. For gh-pages, confirm Pages is enabled for the `gh-pages` branch.
