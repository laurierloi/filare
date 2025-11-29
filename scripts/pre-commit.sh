#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
env_dir="$root_dir/.venv-ci"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required (install via https://astral.sh/uv/)" >&2
  exit 1
fi

if ! command -v prettier >/dev/null 2>&1; then
  echo "prettier is required (install like: npm install --global prettier@3)" >&2
  exit 1
fi

cleanup() {
  rm -rf "$env_dir"
}
trap cleanup EXIT

cd "$root_dir"

rm -rf "$env_dir"
uv venv "$env_dir"
uv sync --group dev --python "$env_dir/bin/python"

uv run --python "$env_dir/bin/python" --no-sync black --check src tests
uv run --python "$env_dir/bin/python" --no-sync pytest
uv run --python "$env_dir/bin/python" --no-sync python src/filare/tools/build_examples.py
mkdir -p outputs
cp -r examples outputs/examples
cp -r tutorial outputs/tutorial
prettier --check "docs/**/*.{md,html}"
