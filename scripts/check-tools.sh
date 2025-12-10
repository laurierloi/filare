#!/usr/bin/env bash

set -euo pipefail

# --- tools check ---
# Define all tools required by agents here
REQUIRED_TOOLS=(uv gh git rg fd jq yq just)

# ensure all required tools are installed and availabble in PATH
missing=()
for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        missing+=("$tool")
    fi
done

if [ "${#missing[@]}" -ne 0 ]; then
    echo "ERROR: Missing required CLI tools:"
    for t in "${missing[@]}"; do
        echo "  - $t"
    done
    echo ""
    echo "Install them before running agents."
    exit 1
fi

echo "All required tools are installed."
