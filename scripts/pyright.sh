#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

export UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}"

# Run pyright using project-managed environment and config in pyproject.toml.
uv run pyright "$@"
