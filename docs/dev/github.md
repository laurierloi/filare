# GitHub CLI for Filare

Use the GitHub CLI (`gh`) to keep day-to-day tasks repeatable: opening PRs against `beta`, applying labels, inspecting CI runs, and scripting repo settings.

## Install `gh`

- macOS (Homebrew): `brew update && brew install gh` (or `brew upgrade gh`).
- Ubuntu/Debian:
  ```
  type -p curl >/dev/null || sudo apt-get install curl -y
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
  sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
  sudo apt-get update
  sudo apt-get install gh
  ```
- Fedora/RHEL/CentOS:
  ```
  sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
  sudo dnf install gh
  ```
- Windows (winget): `winget install --id GitHub.cli -e`

Verify with `gh version`. Authenticate once with `gh auth login` (choose HTTPS, browser flow or paste a PAT).

## Common commands

- Clone: `gh repo clone laurierloi/filare`
- Create PR to `beta`: `gh pr create --base beta --title "feat: ..." --body "..."` (ensure your branch follows `<role>/<desc>`).
- List PRs: `gh pr list --base beta`
- Check CI runs: `gh run list` and `gh run view <id>`

## Managing labels (for the beta → main gate)

If your `gh` build supports label commands:

- Create: `gh label create validated --color 0E8A16 --description "Approved for beta→main promotion"`
- List: `gh label list`

If label subcommands are unavailable, use the REST API helper (requires `gh auth login`):

```
OWNER=laurierloi
REPO=filare
gh api --method POST repos/$OWNER/$REPO/labels \
  -f name=validated \
  -f color=0E8A16 \
  -f description="Approved for beta→main promotion"
```

To label a PR: `gh pr edit <number> --add-label validated` (or `gh api repos/$OWNER/$REPO/issues/<number>/labels -f labels='["validated"]'`).

## Default branch tip

Set the repository default branch to `beta` in the GitHub web UI (Settings → Branches) so new PRs target `beta` by default. The `pr-target-beta` workflow enforces this policy on every PR.
