#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$root_dir"

commit_sha=$(git rev-parse --verify HEAD)
outdir="$root_dir/outputs/bisect/$commit_sha"

venv="$root_dir/.venv"
python_bin="$venv/bin/python"

if [ ! -x "$python_bin" ]; then
  uv venv "$venv"
  uv sync --group dev --python "$python_bin"
fi

echo "Running filare examples/all-document/all-h1.yml -d examples/all-document/metadata.yml -f hs -o $outdir"
rm -rf "$outdir"
mkdir -p "$outdir"

UV_PROJECT_ENVIRONMENT="$venv" UV_PYTHON="$python_bin" \
  uv run --python "$python_bin" --no-sync filare examples/all-document/all-h1.yml -d examples/all-document/metadata.yml -f hs -o "$outdir" >/tmp/filare-bisect.log 2>&1

if [ ! -f "$outdir/all-h1.html" ] || [ ! -f "$outdir/all-h1.svg" ]; then
  echo "expected all-h1.html and all-h1.svg in $outdir" >&2
  exit 1
fi
