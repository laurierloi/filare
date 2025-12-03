#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

src="$root_dir/README.md"
dest="$root_dir/docs/README.md"

if [ ! -f "$src" ]; then
  echo "Missing $src; cannot sync README into docs" >&2
  exit 1
fi

cp "$src" "$dest"
