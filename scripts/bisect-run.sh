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

echo "Running filare examples/ex08.yml -d examples/metadata.yml -f hs -o $outdir"
rm -rf "$outdir"
mkdir -p "$outdir"

UV_PROJECT_ENVIRONMENT="$venv" UV_PYTHON="$python_bin" \
  uv run --python "$python_bin" --no-sync filare examples/ex08.yml -d examples/metadata.yml -f hs -o "$outdir" >/tmp/filare-bisect.log 2>&1

if [ ! -f "$outdir/ex08.html" ] || [ ! -f "$outdir/ex08.svg" ]; then
  echo "expected ex08.html and ex08.svg in $outdir" >&2
  exit 1
fi
