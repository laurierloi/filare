# justfile for Filare
# All commands ensure the agent environment is set up first.

set shell := ["bash", "-cu"]

setup := "source scripts/agent-setup.sh >/dev/null"
import "agents/justfile"

default:
  @echo "Available recipes:"
  @echo "  just version                 # get the current filare version"
  @echo "  just lint                    # run pre-commit on all files"
  @echo "  just pre-commit              # run pre-commit on staged files"
  @echo "  just review                  # interactive review with the operator"
  @echo "  just get-structured-review   # format the operator feedback for agent consumption"
  @echo "  just apply-feedback          # apply operator feedback"
  @echo "  just git-status              # show git status"
  @echo "  just test-all                # run all tests"
  @echo "  just test-fast               # run fast tests (excluding functional)"
  @echo "  just test-functional         # run only functional tests"
  @echo "  just test-specific <path> -- <pytest args> # run a specific test path with extra pytest args"
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
  @echo "  just agent-just-commands     # process the just commands for the agent"
  @echo "  just agent-prompt-gen        # generate the agent prompts"
  @echo "  just agent-prompt-link       # link the agent prompts dir (MUST NOT BE USED BY AGENTS)"
  @echo "  just install-deps            # install dependencies (MUST NOT BE USED BY AGENTS)"
  @echo "  just mermaid-gantt           # generate Mermaid Gantt from backlog headers"
  @echo "  just mermaid-gantt-check     # generate Mermaid Gantt and validate mermaid syntax"
  @echo "  just check-backlog-headers   # validate backlog headers/UIDs"
  @echo "  just taskwarrior-export      # export backlog to Taskwarrior JSON"
  @echo "  just taskwarrior-backfill    # dry-run backfill from Taskwarrior JSON"
  @echo "  just taskwarrior-backfill-apply # apply backfill updates from Taskwarrior JSON"
  @echo "  just timeline-graphviz       # generate Graphviz timeline/timeline.svg"
  @echo "  just codex-container-build   # build codex-ready Docker image"
  @echo "  just codex-container-sh      # start shell in codex Docker image (bind-mount repo)"
  @echo "  just codex-container-run     # run codex container with workspace/env/ssh key"

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

# ---- Operator interaction ----

# ----------------------------------------------------
# REVIEW COMMAND (interactive)
# ----------------------------------------------------
# Usage:
#   just review agent_role="FIXER" task_id="42"
#
# Optional:
#   diff_base="origin/beta"
#
# Example:
#   just review \
#       agent_role="FEATURE" \
#       task_id="88" \
#       diff_base="origin/main"
#
review agent_role task_id diff_base="origin/beta" apply_cmd="":
  {{setup}} && \
  uv run python scripts/review_changes.py \
      --agent-role "{{agent_role}}" \
      --task-id "{{task_id}}" \
      --diff-base "{{diff_base}}"

# ----------------------------------------------------
# GET STRUCTURED REVIEW (agent-friendly, read-only)
# ----------------------------------------------------
# Usage:
#   just get-structured-review agent_role="FIXER" task_id="42"
#
# This prints the contents of:
#   outputs/review/<agent_role>-<task_id>-<step_index>/
# in a structured format the agent can parse.
#
get-structured-review agent_role task_id:
  {{setup}} && \
  uv run python scripts/get_structured_review.py \
      --agent-role "{{agent_role}}" \
      --task-id "{{task_id}}"

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

# Run a specific test path with optional pytest arguments
test-specific target *pytest_args:
  {{setup}} && uv run pytest {{target}} {{pytest_args}}

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

# Process the just commands into agent prompts
agent-just-commands:
  {{setup}} && uv run python scripts/generate_filare_agent_commands.py --justfile justfile --output agents/filare_commands.yml

# Generate Codex prompt markdown files for all agent commands
agent-prompt-gen:
  {{setup}} && uv run python scripts/generate_agent_prompts.py

# Link the agent-prompt to the codex config
agent-prompt-link:
  ln -sf $(pwd)/agents/prompts ~/.codex/prompts

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

# List next ready tasks for a role from Taskwarrior export
taskwarrior-next role="" limit="10":
	set -euo pipefail
	role_args=()
	if [ -n "{{role}}" ]; then
	role_args=(--roles {{role}})
	fi
	{{setup}} && uv run python scripts/taskwarrior_next.py --input outputs/workplan/taskwarrior.json --limit {{limit}} "${role_args[@]}"

# Split Taskwarrior backlog into dependency-safe pools
taskwarrior-pools pools="2":
	{{setup}} && uv run python scripts/taskwarrior_split_pools.py --pools {{pools}} --input outputs/workplan/taskwarrior.json --outdir outputs/workplan

# Update a Taskwarrior task (status/notes) in the export; can stamp completion time
taskwarrior-update uid status="" note="" done="false":
	set -euo pipefail
	args=(--uid {{uid}})
	if [ -n "{{status}}" ]; then
	args+=(--status {{status}})
	fi
	if [ -n "{{note}}" ]; then
	args+=(--note "{{note}}")
	fi
	if [ "{{done}}" = "true" ]; then
	args+=(--done)
	fi
	{{setup}} && uv run python scripts/taskwarrior_update.py --input outputs/workplan/taskwarrior.json "${args[@]}"

# Generate a branch name from a Taskwarrior task UID (optionally check out)
taskwarrior-branch uid checkout="false":
	set -euo pipefail
	branch=$( {{setup}} && uv run python scripts/taskwarrior_branch.py --input outputs/workplan/taskwarrior.json --uid {{uid}} {{ if checkout == "true" { "--checkout" } else { "" } }} )
	echo "$branch"

# Generate Graphviz timeline (DOT + optional SVG)
timeline-graphviz:
  {{setup}} && uv run python scripts/generate_graphviz_timeline.py

# Build codex-ready container image
codex-container-build:
  docker build -f docker/Dockerfile.codex -t filare-codex .

# Start a shell in the codex container with repo bind-mounted and host UID/GID
codex-container-sh:
  docker run --rm -it \
    -v "$PWD":/home/agent/workspace \
    -v "$HOME"/.codex:/home/agent/.codex \
    -w /home/agent/workspace \
    --user $(id -u):$(id -g) \
    filare-codex bash

codex-container-run:
  SSH_KEY=${SSH_KEY:?set SSH_KEY} ENV_FILE=${ENV_FILE:?set ENV_FILE} WORKSPACE=${WORKSPACE:-$PWD} ./scripts/run_codex_container.sh --ssh-key "$SSH_KEY" --env-file "$ENV_FILE" --workspace "$WORKSPACE"

# Orchestrator CLI wrappers (PYTHONPATH scoped to agents/src)

# Install tools - MUST NOT BE USED BY AGENTS
install-deps:
  bash scripts/install-deps.sh
