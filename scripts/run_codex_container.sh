#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: run_codex_container.sh --ssh-key PATH --env-file PATH [--workspace PATH] [--image NAME]

Required:
  --ssh-key PATH     Private SSH key on host to mount at /home/agent/.ssh/id_rsa (read-only).
  --env-file PATH    .env file with environment variables for the agent (mounted via --env-file).

Optional:
  --workspace PATH   Host workspace directory to bind to /home/agent/workspace (default: $PWD).
                     If the directory does not exist or is empty, it will be created and populated
                     with the contents of the current working directory as a template.
  --image NAME       Docker image name (default: filare-codex).

Notes:
  - Host ~/.codex is mounted to /home/agent/.codex.
  - Container runs with host UID/GID via --user $(id -u):$(id -g).
EOF
}

workspace="${PWD}"
image="filare-codex"
ssh_key=""
env_file=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace)
      workspace="$2"; shift 2;;
    --ssh-key)
      ssh_key="$2"; shift 2;;
    --env-file)
      env_file="$2"; shift 2;;
    --image)
      image="$2"; shift 2;;
    -h|--help)
      usage; exit 0;;
    *)
      echo "Unknown argument: $1" >&2; usage; exit 1;;
  esac
done

if [[ -z "$ssh_key" ]]; then
  echo "Missing required --ssh-key" >&2; usage; exit 1
fi
if [[ -z "$env_file" ]]; then
  echo "Missing required --env-file" >&2; usage; exit 1
fi

workspace="$(realpath "$workspace")"
ssh_key="$(realpath "$ssh_key")"
env_file="$(realpath "$env_file")"

if [[ ! -f "$ssh_key" ]]; then
  echo "SSH key not found: $ssh_key" >&2; exit 1
fi
if [[ ! -f "$env_file" ]]; then
  echo "Env file not found: $env_file" >&2; exit 1
fi

# Prepare workspace: if missing or empty, seed from current repo.
if [[ ! -d "$workspace" ]]; then
  mkdir -p "$workspace"
fi
if [[ -z "$(ls -A "$workspace")" ]]; then
  echo "Seeding workspace from $PWD into $workspace"
  rsync -a "$PWD"/ "$workspace"/
fi

codex_dir="${HOME}/.codex"
mkdir -p "$codex_dir"

# Prepare temporary .ssh with key only; user manages known_hosts inside container if needed
ssh_tmp="$(mktemp -d)"
trap 'rm -rf "$ssh_tmp"' EXIT
install -m 700 -d "$ssh_tmp"
install -m 600 "$ssh_key" "$ssh_tmp/id_rsa"

docker run --rm -it \
  -v "$workspace":/home/agent/workspace \
  -v "$codex_dir":/home/agent/.codex \
  -v "$ssh_tmp":/home/agent/.ssh:ro \
  --env-file "$env_file" \
  -e HOME=/home/agent \
  -e GIT_SSH_COMMAND="ssh -F /home/agent/.ssh/config" \
  -w /home/agent/workspace \
  --user $(id -u):$(id -g) \
  "$image" bash
