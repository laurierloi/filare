# justfile for Filare
# All commands ensure the agent environment is set up first.

set shell := ["bash", "-cu"]

setup := "source scripts/agent-setup.sh >/dev/null"

default:
  @echo "Available recipes:"
  @echo "  just version                 # get the current filare version"
  @echo "  just lint                    # run pre-commit on all files"
  @echo "  just pre-commit              # run pre-commit on staged files"
  @echo "  just test-all                # run all tests"
  @echo "  just test-fast               # run fast tests (excluding functional)"
  @echo "  just test-functional         # run only functional tests"
  @echo "  just test-mermaid            # test the mermaid diagrams generation"
  @echo "  just test-semantic-release   # test semantic-release configuration"
  @echo "  just test-version            # see what would be the next version"
  @echo "  just example-first           # build first example (ex01)"
  @echo "  just demo-first              # build first example (demo01)"
  @echo "  just build-docs              # build mkdocs documentation"
  @echo "  just build-examples          # rebuild all examples"
  @echo "  just bom-check               # run filare-qty BOM sanity check"
  @echo "  just check-tools             # verify required CLI tools are present"
  @echo "  just install-deps            # install dependencies (MUST NOT BE USED BY AGENTS)"
  @echo "  just mermaid-gantt           # generate Mermaid Gantt from backlog headers"

# ---- Version ----
version:
  cat VERSION

# ---- Linting & hooks ----

# Lint: run lint script
lint:
  {{setup}} && ./scripts/lint.sh

# Run pre-commit only on staged/changed files
pre-commit:
  {{setup}} && uv run pre-commit run

# ---- Git ----
git-status:
  {{setup}} && git status -sb

# ---- Testing ----

# all tests
test-all:
  {{setup}} && uv run pytest --include-functional

# All tests unit tests
test-fast:
  {{setup}} && uv run pytest

# Only functional tests (expects tests marked with "functional")
test-functional:
  {{setup}} && uv run pytest -m functional

test-mermaid:
  {{setup}} && ./scripts/check-mermaid.sh

test-semantic-release:
  {{setup}} && npx semantic-release --dry-run --noop --stdout --yes

test-version:
  {{setup}} && npx semantic-release --version --dry-run --noop --stdout --yes

# ---- Filare commands & docs ----

# Build only the first example with filare (quick sanity run)
example-first:
  {{setup}} && uv run filare run examples/ex01.yml -f hpst -o outputs

# Build only the first example with filare (quick sanity run)
demo-first:
  {{setup}} && uv run filare run examples/demo01.yml -f hpst -o outputs

# Show resolved Filare settings (YAML, includes defaults)
filare-settings-get:
  {{setup}} && uv run filare settings show --format yaml --include-defaults

# Build full documentation with mkdocs
build-docs:
  {{setup}} && uv run mkdocs build

# Rebuild all examples/tutorials via the tools script
build-examples:
  {{setup}} && uv run python src/filare/tools/build_examples.py

# BOM sanity check using filare-qty
bom-check:
  {{setup}} && uv run filare qty tests/bom/bomqty.yml

# ---- Tooling ----

# Check that all required CLI tools are installed (uses your check-tools.sh)
check-tools:
  {{setup}} && bash scripts/check-tools.sh

# Generate Mermaid Gantt from backlog headers
mermaid-gantt:
  {{setup}} && uv run python scripts/generate_mermaid_gantt.py

# Install tools - MUST NOT BE USED BY AGENTS
install-deps:
  bash scripts/install-deps.sh
