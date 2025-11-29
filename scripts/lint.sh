#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required (install via https://astral.sh/uv/)" >&2
  exit 1
fi

cd "$root_dir"

uv run black src tests
prettier --write "docs/**/*.{md,html}" "src/filare/templates/**/*.html"
