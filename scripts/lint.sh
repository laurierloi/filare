#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required (install via https://astral.sh/uv/)" >&2
  exit 1
fi

if ! command -v prettier >/dev/null 2>&1; then
  echo "prettier is required (install globally: npm install --global prettier@3)" >&2
  exit 1
fi

cd "$root_dir"

# Try to fix
uv run black src tests
prettier --write "docs/**/*.{md,html}" "src/filare/templates/**/*.html"

# Check
uv run black --check src tests
prettier --check "docs/**/*.{md,html}" "src/filare/templates/**/*.html"
