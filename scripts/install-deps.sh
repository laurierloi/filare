#!/usr/bin/env bash
set -euo pipefail

scripts_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#
# Define all tools required by agents here
REQUIRED_TOOLS=(uv gh git rg fd jq yq just)

# Map tool -> version to install/check
declare -A TOOL_VERSIONS=(
  [uv]="0.9.15"
  [gh]="2.83.1"
  [git]="2.52.0"
  [rg]="15.0.0"
  [fd]="10.2.0"
  [jq]="1.8.1"
  [yq]="4.49.2"
  [just]="1.43.1"
)

# Install required tools
for tool in "${REQUIRED_TOOLS[@]}"; do
  version="${TOOL_VERSIONS[$tool]}"
  echo "Installing $tool version $version..."
  ${scripts_dir}/install-tool.sh "$tool" "$version"
done
