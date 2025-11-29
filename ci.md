# Filare CI Pipeline

This repository uses a GitHub Actions workflow (`.github/workflows/ci.yml`) that runs on pushes and pull requests to `main`. It is split into staged jobs so you can see where failures occur and reuse artifacts across steps.

## Jobs / Stages

1. **Lint**
   - Runs `black --check` on `src/` and `tests/`.
   - Runs `prettier --check` on docs and templates.
   - Requires Python (3.11) and Node (for prettier).

2. **Tests**
   - Installs graphviz and project + dev deps.
   - Runs `pytest`.
   - Uses the same Python version as lint.

3. **Build examples/templates**
   - Installs graphviz + project.
   - Runs `filare` to generate outputs from examples/tutorials.
   - Uploads `outputs/` as an artifact for later stages.

4. **Docs / gh-pages (main only)**
   - Copies `docs/` into `site/` and includes built example artifacts if present.
   - Publishes `site/` to GitHub Pages via `peaceiris/actions-gh-pages`.

5. **Release (semantic-release, main only)**
   - Uses `python-semantic-release` to bump the version and publish release assets.
   - Needs `GH_TOKEN` (GitHub token) and `PYPI_TOKEN` (if publishing to PyPI through semantic-release).

6. **Publish to PyPI (main only)**
   - Builds the distribution (`python -m build`).
   - Uploads via `twine` using `PYPI_TOKEN`.

7. **Verify PyPI**
   - Installs `filare` from PyPI and checks `filare --help`.

8. **Container (GHCR)**
   - Builds a Docker image and pushes to `ghcr.io/${{ github.repository }}:latest`.
   - Uses `GITHUB_TOKEN` for registry auth.

## Required Secrets

- `PYPI_TOKEN`: PyPI API token for publishing.
- `GH_TOKEN`: (optional) used by semantic-release for tagging; `GITHUB_TOKEN` provided by Actions is usually sufficient.
- GitHub Pages and GHCR steps use the built-in `GITHUB_TOKEN`.

## Local Reproduction

- Lint: `black --check src tests` and `prettier --check "docs/**/*.{md,html}" "src/filare/templates/**/*.html"`.
- Tests: `pytest` (ensure `graphviz` is installed).
- Examples: `filare -f hs -o outputs/examples examples/demo01.yml`.
- Build dist: `python -m build`.
- Docker: `docker build -t filare-local .`.

## Creating/Updating the Pipeline

1. Edit `.github/workflows/ci.yml` to adjust stages, Python/Node versions, or paths.
2. Ensure secrets (`PYPI_TOKEN`) are set in the repo settings.
3. Push to `main` to exercise all stages; PRs run lint/tests/examples.
4. For gh-pages, confirm Pages is enabled for the `gh-pages` branch.
