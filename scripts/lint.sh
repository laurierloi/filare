#!/usr/bin/env bash

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required (install via https://astral.sh/uv/)" >&2
  exit 1
fi

if ! command -v prettier >/dev/null 2>&1; then
  echo "prettier is required (install globally: npm install --global prettier@3)" >&2
  exit 1
fi

# Check
echo "Running black"
uv run black --check src tests
if [ $? -ne 0 ]; then
    echo "Code is not properly formatted. Running black formatter..."
    uv run black src tests
fi

echo "Running prettier"
prettier --check "docs/**/*.{md,html}"
if [ $? -ne 0 ]; then
    echo "Documentation is not properly formatted. Running prettier formatter..."
    prettier --write "docs/**/*.{md,html}"
fi

echo "Running pyright"
uv run pyright src
