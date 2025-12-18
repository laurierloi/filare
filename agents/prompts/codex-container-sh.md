---
description: Start a shell in the codex container with repo bind-mounted and host
  UID/GID
---

Start a shell in the codex container with repo bind-mounted and host UID/GID
Category: misc.

Command to run inside the repo:
```bash
source scripts/agent-setup.sh >/dev/null && just codex-container-sh
```
After execution, summarize the outcome succinctly and mention any errors or next steps.
