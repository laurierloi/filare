#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

if ! command -v mmdc >/dev/null 2>&1; then
  echo "mmdc (mermaid-cli) is required. Install with: npm install --global @mermaid-js/mermaid-cli@11.12.0" >&2
  exit 1
fi

# Puppeteer opts: disable sandbox so GitHub-hosted runners (and locked-down containers) can launch Chromium.
puppeteer_cfg="$tmpdir/puppeteer.json"
cat >"$puppeteer_cfg" <<'CFG'
{
  "launchOptions": {
    "args": ["--no-sandbox", "--disable-setuid-sandbox"]
  }
}
CFG

failed_list=""
files_override=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --failed-list)
      failed_list="$2"
      shift 2
      ;;
    --files)
      files_override="$2"
      shift 2
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -n "$files_override" ]]; then
  # Comma or space separated list.
  IFS=', ' read -r -a files <<<"$files_override"
else
  mapfile -t files < <(rg -l '```mermaid' "$root_dir/docs" || true)
fi

if [ "${#files[@]}" -eq 0 ]; then
  echo "No Mermaid diagrams found under docs/"
  exit 0
fi

idx=0
status=0
failed_output="$root_dir/mermaid_failed.txt"
> "$failed_output"

if [[ -n "$failed_list" ]]; then
  mapfile -t to_rerun <"$failed_list"
  echo "Re-running failed Mermaid blocks from $failed_list"
  for line in "${to_rerun[@]}"; do
    f="${line%% *}"
    blk="${line##* }"
    echo "Rechecking $f (block $blk)"
    block="$(python3 - "$f" "$blk" <<'PY'
import sys, re, pathlib
path = pathlib.Path(sys.argv[1])
target = int(sys.argv[2])
blocks = re.findall(r"```mermaid\n(.*?)\n```", path.read_text(), flags=re.DOTALL)
if target < 0 or target >= len(blocks):
    raise SystemExit(f"Invalid block index {target} for {path}")
sys.stdout.write(blocks[target])
PY
)"
    outfile="$tmpdir/$idx.mmd"
    printf "%s\n" "$block" >"$outfile"
    if ! mmdc -p "$puppeteer_cfg" -i "$outfile" -o "$tmpdir/$idx.svg" >/dev/null 2>&1; then
      echo "Mermaid parse/render failed for $f (block $blk)" >&2
      status=1
    else
      echo "✓ Mermaid parsed/rendered: $f (block $blk)"
    fi
    idx=$((idx + 1))
  done
else
  for f in "${files[@]}"; do
    echo "Checking Mermaid blocks in: $f"
    block_idx=0
    while IFS= read -r -d '' block; do
      outfile="$tmpdir/$idx.mmd"
      printf "%s\n" "$block" >"$outfile"
      if ! mmdc -p "$puppeteer_cfg" -i "$outfile" -o "$tmpdir/$idx.svg" >/dev/null 2>&1; then
        echo "Mermaid parse/render failed for $f (block $block_idx)" >&2
        printf "%s %s\n" "$f" "$block_idx" >>"$failed_output"
        status=1
        echo "---- failing block content ($f block $block_idx) ----" >&2
        printf "%s\n" "$block" >&2
        echo "-----------------------------------------------------" >&2
      else
        echo "✓ Mermaid parsed/rendered: $f (block $block_idx)"
      fi
      idx=$((idx + 1))
      block_idx=$((block_idx + 1))
    done < <(python3 - "$f" <<'PY'
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
fi

if [[ $status -ne 0 ]]; then
  echo "Mermaid check completed with failures. To rerun failed blocks only:"
  echo "  ./scripts/check-mermaid.sh --failed-list $failed_output"
else
  echo "Mermaid check completed successfully."
  rm -f "$failed_output"
fi

exit $status
