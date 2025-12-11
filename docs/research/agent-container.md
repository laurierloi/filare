# Codex CLI Agent Container (Filare)

## Summary
Specification for a Docker image that bundles Filare tooling plus Codex CLI prerequisites, supports host UID/GID mapping, and allows bind-mounting the repo so changes persist. Includes tmux/neovim for operator comfort and headless Chromium/Playwright for tests.

## Key Points
- Image: `docker/Dockerfile.codex` installs uv/gh/git/rg/fd/jq/yq/just, Graphviz, npm, mermaid-cli, Playwright/Chromium, tmux, neovim, fonts, git-lfs.
- Build: `just codex-container-build` (tags `filare-codex`).
- Shell: `just codex-container-sh` uses `--user $(id -u):$(id -g)` and `-v $PWD:/workspace` so files are host-owned and persistent.
- Host dotfiles: bind-mount optional `~/.tmux.conf` and `~/.config/nvim` into the container for familiar tmux/NVim configs. Bind `~/.codex` to `/root/.codex` to reuse host Codex config/session.
- Codex credentials: use host `~/.codex` mount; avoid baking secrets into the image.
- Branch sync: mount the repo so you control branch/cleanliness; otherwise clone in the container entry if needed.

## Next Steps
- Add `just codex-container-sh` variants to inject env files for Codex creds.
- Optional: entrypoint to auto-clone/checkout a branch when repo is not mounted.
- Optional: volume for uv cache to speed repeated runs.
