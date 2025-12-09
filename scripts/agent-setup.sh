#!/usr/bin/env bash
set -euo pipefail

# Optional first argument: path to env file (relative to repo root or absolute).
# Defaults to ".env" at the root of the git repo.
ENV_FILE_ARG="${1:-}"

# --- Ensure we are inside a git repo and get repo root ---
if ! repo_root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  echo "ERROR: agent_setup.sh must be run inside a git repository." >&2
  exit 1
fi

# Resolve env file path
if [[ -z "$ENV_FILE_ARG" ]]; then
  ENV_FILE="$repo_root/.env"
elif [[ "$ENV_FILE_ARG" = /* ]]; then
  ENV_FILE="$ENV_FILE_ARG"
else
  ENV_FILE="$repo_root/$ENV_FILE_ARG"
fi

# --- Load environment file (required) ---
if [[ ! -f "$ENV_FILE" ]]; then
  echo "ERROR: env file '$ENV_FILE' not found." >&2
  echo "       Provide an env file as ./agent_setup.sh [env_file] and ensure it defines GH_TOKEN." >&2
  exit 1
fi

echo "Loading environment from: $ENV_FILE"
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

# --- Git: force non-interactive, no editors ---
git config core.editor true
git config sequence.editor true
git config merge.autoEdit no
git config core.pager cat

echo "Git configured for non-interactive, editorless operation in this repo."

# --- GitHub CLI: non-interactive auth setup (optional, if gh is installed) ---
if command -v gh >/dev/null 2>&1; then
  export GH_PROMPT_DISABLED=1

  if gh auth status --hostname github.com >/dev/null 2>&1; then
    echo "gh: already authenticated for github.com."
  else
    # Require GH_TOKEN if not already authenticated
    if [[ -z "${GH_TOKEN-}" ]]; then
      echo "ERROR: gh is not authenticated for github.com, and GH_TOKEN is not set in '$ENV_FILE'." >&2
      echo "       Either:" >&2
      echo "         1) Add GH_TOKEN to '$ENV_FILE', OR" >&2
      echo "         2) Run 'gh auth login --hostname github.com --git-protocol ssh' manually," >&2
      echo "            then re-run ./agent_setup.sh." >&2
      exit 1
    fi

    echo "gh: logging in to github.com using GH_TOKEN from '$ENV_FILE'..."
    echo "$GH_TOKEN" | gh auth login \
      --hostname github.com \
      --git-protocol ssh \
      --with-token >/dev/null
    echo "gh: authentication configured for github.com."
  fi
else
  echo "gh: GitHub CLI not found; skipping GitHub authentication."
fi

# --- UV: ensure that the cache is always the same
export UV_CACHE_DIR="${repo_root}/.uv-cache"
mkdir -p "$UV_CACHE_DIR"
echo "UV cache directory set to: $UV_CACHE_DIR"

# --- UV: ensure that the environment is configured
if [[ ! -d ".venv"  ]]; then
  echo "No .venv found. Initializing environment with uv sync..."
  uv sync --group dev
else
  echo ".venv already present. Skipping uv sync."
fi


# --- Pre-commit: ensure that it is setup
uv run pre-commit install
