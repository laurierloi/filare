# Codex container

The Codex image (`docker/Dockerfile.codex`) is a ready-to-use environment for Filare agents with uv, GitHub CLI, Graphviz, ripgrep/fd/jq/yq/just, Node/npm, mermaid-cli, `@openai/codex`, Playwright/Chromium, tmux, neovim, fonts, and git-lfs.

## Build the image

- `source scripts/agent-setup.sh >/dev/null && just codex-container-build` builds `filare-codex` locally.
- Equivalent raw Docker: `docker build -f docker/Dockerfile.codex -t filare-codex .`

## Open an interactive shell

- `source scripts/agent-setup.sh >/dev/null && just codex-container-sh`
- Binds the current repo to `/home/agent/workspace`, mounts host `~/.codex`, and runs as your UID/GID so file ownership stays correct.

## Run with SSH key and env file

- `SSH_KEY=/path/to/id_rsa ENV_FILE=/path/to/.env [WORKSPACE=/path/to/workspace] source scripts/agent-setup.sh >/dev/null && just codex-container-run`
- Wraps `scripts/run_codex_container.sh`, which:
  - Seeds an empty `WORKSPACE` from the current repo.
  - Mounts host `~/.codex` to `/home/agent/.codex`.
  - Mounts a temporary `.ssh` containing only the provided key (read-only); manage `known_hosts` inside the container as needed.
  - Runs as your UID/GID with `HOME=/home/agent`.

## Notes

- The container default command is `bash`; override with `docker run ... filare-codex <command>` if needed.
- Keep secrets out of the image—use the mounted `.env`/`.codex` files instead.
