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
  @echo "  just check-overlap           # run filare-check-overlap over all html files in outputs/"
  @echo "  just bom-check               # run filare-qty BOM sanity check"
  @echo "  just check-tools             # verify required CLI tools are present"
  @echo "  just install-deps            # install dependencies (MUST NOT BE USED BY AGENTS)"
  @echo "  just mermaid-gantt           # generate Mermaid Gantt from backlog headers"
  @echo "  just mermaid-gantt-check     # generate Mermaid Gantt and validate mermaid syntax"
  @echo "  just check-backlog-headers   # validate backlog headers/UIDs"
  @echo "  just taskwarrior-export      # export backlog to Taskwarrior JSON"
  @echo "  just taskwarrior-backfill    # dry-run backfill from Taskwarrior JSON"
  @echo "  just taskwarrior-backfill-apply # apply backfill updates from Taskwarrior JSON"
  @echo "  just timeline-graphviz       # generate Graphviz timeline/timeline.svg"

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
  {{setup}} && uv run filare run examples/basic/basic01.yml -d examples/basic/metadata.yml -f hpst -o outputs

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

# Check for overlapping elements in all generated HTML files in outputs/
check-overlap:
  {{setup}} && uv run filare-check-overlap outputs/*.html


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

# Generate and validate the Mermaid Gantt diagram
mermaid-gantt-check:
  {{setup}} && uv run python scripts/generate_mermaid_gantt.py
  {{setup}} && ./scripts/check-mermaid.sh --files docs/workplan/gantt.md

# Validate backlog headers and UID formats
check-backlog-headers:
  {{setup}} && uv run python scripts/check_backlog_headers.py

# Export backlog to Taskwarrior JSON (filters can be passed as CLI args)
taskwarrior-export:
  {{setup}} && uv run python scripts/export_taskwarrior.py

# Backfill headers from Taskwarrior JSON (dry-run)
taskwarrior-backfill:
  {{setup}} && uv run python scripts/taskwarrior_backfill.py outputs/workplan/taskwarrior.json

# Backfill headers from Taskwarrior JSON (apply changes)
taskwarrior-backfill-apply:
  {{setup}} && uv run python scripts/taskwarrior_backfill.py --apply outputs/workplan/taskwarrior.json

# Generate Graphviz timeline (DOT + optional SVG)
timeline-graphviz:
  {{setup}} && uv run python scripts/generate_graphviz_timeline.py

# Install tools - MUST NOT BE USED BY AGENTS
install-deps:
  bash scripts/install-deps.sh
