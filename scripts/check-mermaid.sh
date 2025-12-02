#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

if ! command -v mmdc >/dev/null 2>&1; then
  echo "mmdc (mermaid-cli) is required. Install with: npm install --global @mermaid-js/mermaid-cli@11.12.0" >&2
  exit 1
fi

mapfile -t files < <(rg -l '```mermaid' "$root_dir/docs" || true)

if [ "${#files[@]}" -eq 0 ]; then
  echo "No Mermaid diagrams found under docs/"
  exit 0
fi

idx=0
status=0
for f in "${files[@]}"; do
  # Extract each mermaid block to its own file
  while IFS= read -r -d '' block; do
    outfile="$tmpdir/$idx.mmd"
    printf "%s\n" "$block" >"$outfile"
    if ! mmdc -i "$outfile" -o "$tmpdir/$idx.svg" >/dev/null 2>&1; then
      echo "Mermaid parse/render failed for $f (block $idx)" >&2
      status=1
    fi
    idx=$((idx + 1))
  done < <(python - "$f" <<'PY'
import sys, re, pathlib
path = pathlib.Path(sys.argv[1])
text = path.read_text()
blocks = re.findall(r"```mermaid\n(.*?)\n```", text, flags=re.DOTALL)
for b in blocks:
    sys.stdout.buffer.write(b.encode("utf-8"))
    sys.stdout.buffer.write(b"\0")
PY
)
done

exit $status
